import datetime

from django.contrib.auth.decorators import login_required
import json

from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import F, Sum, Max, Min, Avg, Count

from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, FileResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt


from mAuth.models import User
from .models import *


def json_response(code, msg, **kwargs):
    res = {
        'code': code,
        'msg': msg,
    }
    res.update(kwargs)
    return JsonResponse(res)


def manager_login_required(func):
    def wrapper(req, *args, **kwargs):
        if not req.user.is_admin:
            return HttpResponseForbidden()
        return func(req, *args, **kwargs)
    return wrapper


def login_required_json(func):
    def wrapper(req, *args, **kwargs):
        if not req.user.is_authenticated:
            return json_response(1024, "success", redirect=settings.LOGIN_URL)
        return func(req, *args, **kwargs)
    return wrapper


def collection(req, label):
    if req.GET.get("page", None):
        # 草稿商品的列表
        page = req.GET["page"]
        try:
            # 分类商品列表
            c = Collection.objects.get(label=label)
            goods = c.good_set.filter(is_sell=True)
        except Collection.DoesNotExist:
            # 标签不存在选全部
            goods = Good.objects.filter(is_sell=True)

        res = []
        for good in goods:
            res.append(good.to_first_view())
        return json_response(0, "success", list=res)
    return render(req, "order/shop_item.html")


def view_good(req, good_id):
    good = Good.objects.get(id=good_id, is_sell=True)
    if req.user and req.user.is_authenticated:
        # 增加浏览记录
        GoodTrack.objects.create(good=good, user=req.user)
    return render(req, "order/item_detail.html", {"good": good})


@login_required
def my_order(req):
    if req.method == "GET":
        orders = Order.objects.filter(user=req.user)
        return render(req, "order/myorder.html", context={
            "orders": orders
        })


@login_required_json
def add_cart(req, good_id):
    if req.method == "POST":
        size = req.POST.get("size", "")
        try:
            cart = Cart.objects.get(user=req.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=req.user)

        now_amount = GoodSize.objects.get(good_id=good_id, size=size).amount
        if now_amount == 0:
            return json_response(1, "库存不足")
        try:
            item = cart.cartitem_set.get(good_id=good_id, size=size)
            if item.amount < now_amount:
                item.amount += 1
                item.save()
            else:
                return json_response(1, "库存不足")
        except CartItem.DoesNotExist:
            if now_amount > 0:
                CartItem.objects.create(amount=1, size=size, good_id=good_id, cart=cart)
        return json_response(0, "success")


@login_required
def update_cart(req):
    if req.method == "POST":
        real_amount = amount = int(req.POST.get("amount", 0))
        cart_item_id = int(req.POST.get("id", 0))

        if amount == 0:
            CartItem.objects.filter(id=cart_item_id).delete()
        else:
            c_i = CartItem.objects.get(id=cart_item_id)
            now_amount = GoodSize.objects.get(good=c_i.good, size=c_i.size).amount
            real_amount = min(amount, now_amount)
            CartItem.objects.filter(id=cart_item_id).update(amount=real_amount)
        return json_response(0, "success", data={
            "id": cart_item_id,
            "amount": amount,
            "real_amount": real_amount
        })


@login_required
def get_cart(req):
    if req.method == "GET":
        try:
            cart = Cart.objects.get(user=req.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=req.user)

        # 处理库存信息
        items = cart.cartitem_set.all()
        for item in items:
            try:
                # 如果下架的话当作不存在处理
                good_s = GoodSize.objects.get(good=item.good, size=item.size, good__is_sell=True)
                if good_s.amount < item.amount:
                    # 更新item的amount
                    item.amount = good_s.amount
                    item.save()
            except GoodSize.DoesNotExist:
                # 说明该商品已经不存在 直接删除算了
                item.delete()
        return render(req, "order/cart.html", context={
            "carts": Cart.objects.get(user=req.user).cartitem_set.all()
        })


@login_required
def cart_submit(req):
    if req.method == "POST":
        cart = Cart.objects.get(user=req.user)
        no_submit = False  # 是否有没有提交的
        order_item = []  # 需要转换成订单项目的购物车项目
        order = Order(cash=.0, address="请填写地址", user=req.user)
        for c_i in cart.cartitem_set.all():
            try:
                GoodSize.objects.filter(good=c_i.good, size=c_i.size).update(amount=F("amount")-c_i.amount)
                # 计算价格
                order.cash += c_i.amount * c_i.good.price
                # 加入到订单项目
                order_item.append(c_i.to_order_item())
                # 清空对应的项目
                c_i.delete()
            except :
                no_submit = True
        if len(order_item) == 0:
            return json_response(2, "无提交成功项目，均数量不足")
        # 规范化金额
        order.cash = round(order.cash, 2)
        # 创建订单
        order.save()
        for item in order_item:
            # 赋予订单号
            item.order = order
        OrderItem.objects.bulk_create(order_item)
        if no_submit:
            return json_response(1, "已提交部分，剩余库存不足")
        return json_response(0, "全部提交")


@login_required
def order_detail(req, order_id):
    if req.method == "GET":
        try:
            if req.user.is_admin:
                order = Order.objects.get(id=order_id)
            else:
                order = Order.objects.get(id=order_id, user=req.user)
            return render(req, "order/order_detail.html", context={
                "order": order,
                "order_items": order.orderitem_set.all()
            })
        except Order.DoesNotExist:
            return HttpResponseForbidden


@login_required_json
def order_operation(req, order_id, op):
    if req.method == "POST":
        if op == "pay":
            Order.objects.filter(id=order_id).update(
                address=req.POST.get("address", "未填写"), status=Order.PAY, pay_time=datetime.datetime.now())
            return json_response(0, "success")
        elif op == "cancel":
            Order.objects.filter(id=order_id).update(status=Order.CANCEL)
            return json_response(0, "success")
        elif op == "save" and req.user.is_admin:
            Order.objects.filter(id=order_id).update(address=req.POST["address"],
                                                     cash=req.POST["cash"],
                                                     express_number=req.POST["express_number"],
                                                     express_cmp=req.POST["express_cmp"])
            return json_response(0, "success")
        elif op == "ship" and req.user.is_admin:
            try:
                order = Order.objects.get(id=order_id)
                msg = '''订单号：{}\n
                金额 ：￥{}\n
                物流公司：{}\n
                物流单号：{}\n
                寄送地址：{}\n
                '''.format(order.id, order.cash, order.express_cmp, order.express_number,
                           order.address.replace("/", " "))
                send_mail("[DjleeOnlineShop]发货提醒", msg, settings.EMAIL_HOST_USER, [order.user.mail])

                order.status = Order.SHIP,
                order.express_number = req.POST["express_number"],
                order.express_cmp = req.POST["express_cmp"],
                order.ship_time = datetime.datetime.now()
                return json_response(0, "success")
            except Exception as e:
                return json_response(1, "发货失败，请稍后重试")


@manager_login_required
@csrf_exempt
def upload_image(req):
    if req.method == "POST":
        file = req.FILES["img"]
        direction = req.POST["dir"]
        try:
            img = Image.objects.create(img=req.FILES["img"], file_name=file.name,
                                       image_dir=ImageDir.objects.get(direction=direction))
            return json_response(0, "成功", img={
                "src": img.img.url,
                "id": img.id
            })
        except ImageDir.DoesNotExist:
            return json_response(1, "错误")


@manager_login_required
def get_images(req):
    if req.method == "GET":
        direction = req.GET.get("dir", "")
        page = int(req.GET.get("page", 1))
        CLOUD_PAGE_SIZE = 30

        res_images = []
        images = Image.objects.filter(image_dir__direction=direction)[(page - 1) * CLOUD_PAGE_SIZE: page * CLOUD_PAGE_SIZE]
        if images:
            for image in images:
                res_images.append(image.to_json())
        else:
            page -= 1
        return json_response(0, "success", data=res_images, page=page)


@manager_login_required
def manager_good(req, good_id):
    if req.method == "GET":
        good = Good.objects.get(id=good_id)
        print(good.collections)
        collections = []
        for i, c in enumerate(Collection.objects.order_by("index")):
            style = ""
            if i % 5 == 0:
                style = "danger"
            elif i % 5 == 1:
                style = "warning"
            elif i % 5 == 2:
                style = "success"
            elif i % 5 == 3:
                style = "default"
            elif i % 5 == 4:
                style = "primary"
            collections.append({
                "style": style,
                "collection": c,
                "is_select": good.collections.filter(label=c.label).exists()
            })
        return render(req, "order/edit_good.html", context={
            "good": good,
            "style_collections": collections,
            "imageDir": ImageDir.objects.all()
        })
    elif req.method == "POST":
        pass


@login_required
@manager_login_required
@csrf_exempt
def add_good(req):
    if req.method == "GET":
        # 创建草稿
        good = Good.objects.create()
        return redirect("/manager/good/{}/".format(good.id))
    elif req.method == "POST":
        pass


@manager_login_required
def edit_goods(req):
    if req.method == "GET":
        if req.GET.get("page", None):
            # 草稿商品的列表
            page = req.GET["page"]
            goods = Good.objects.filter(is_sell=False)
            res = []
            for good in goods:
                res.append(good.to_first_view())
            return json_response(0, "success", list=res)
        else:
            return render(req, "order/shop_item.html", context={"to_manager_page": True})


@manager_login_required
def update_good(req, good_id):
    if req.method == "POST":
        try:
            good = Good.objects.get(id=good_id)
        except Good.DoesNotExist:
            return json_response(1, "更新错误")
        data = json.loads(req.body)
        print(data)

        good.title = data["title"]
        good.price = data["price"]
        good.content = data["content"]
        good.is_sell = data["is_sell"]
        good.save()

        # 先清楚再插入
        good.collections.clear()
        good.collections.add(*Collection.objects.filter(name__in=data["collections"]))

        # 处理码数
        exist_good_size_ids = []
        for good_size in data["sizes"]:
            # 如果有则更新 没有则创建
            good_size_obj = good.goodsize_set.filter(size=good_size["size"])
            if good_size_obj:
                good_size_obj.update(amount=F("amount") + good_size["add_amount"], index=good_size["index"])
                exist_good_size_ids.append(good_size_obj[0].id)
            else:
                exist_good_size_ids.append(
                    GoodSize.objects.create(good=good, size=good_size["size"], amount=good_size["add_amount"], index=good_size["index"])
                        .id)

        good.goodsize_set.exclude(id__in=exist_good_size_ids).delete()
        # 处理图片
        good.goodimage_set.all().delete()
        need_create_images = []
        for good_image in data["images"]:
            need_create_images.append(
                GoodImage(good=good, image=Image.objects.get(id=good_image["id"]), index=good_image["index"])
            )
        GoodImage.objects.bulk_create(need_create_images)

        return json_response(0, "success")


@manager_login_required
def down_good(req, good_id):
    if req.method == "POST":
        Good.objects.filter(id=good_id).update(is_sell=False)
        return json_response(0, "下架成功")


@manager_login_required
def remove_good(req, good_id):
    if req.method == "POST":
        try:
            Good.objects.get(id=good_id).delete()
            return json_response(0, "删除成功", redirect="/manager/good/")
        except:
            return json_response(1, "删除错误")


@manager_login_required
def manager_collection(req):
    if req.method == "GET":
        cs = Collection.objects.order_by("index")
        return render(req, "order/manager_collection.html", context={"all_collections": cs})
    elif req.method == "POST":
        data = json.loads(req.body)
        for c in data:
            if "id" in c:
                c_id = c.pop("id")
                Collection.objects.filter(id=c_id).update(**c)
            else:
                Collection.objects.create(**c)
        return json_response(0, "success")


@manager_login_required
def manager_order(req):
    if req.method == "GET":
        return render(req, "order/manage-order.html", context={
            "status_lst": Order.STATUS_CHOICES
        })


def get_query_order(params):
    param = dict()
    order_id = params.get("order_id", "")
    status = params.get("status", "")
    from_create_time = params.get("from_create_time", "")
    to_create_time = params.get("from_create_time", "")
    user_mail = params.get("mail", "")
    user_phone = params.get("phone", "")
    good_id = params.get("good_id", "")
    good_title = params.get("title", "")

    if order_id != "":
        param["id"] = int(order_id)
    elif status != "":
        param["status"] = status
    elif from_create_time != "":
        param["create_time__gte"] = datetime.datetime.strptime(from_create_time, "%Y-%m-%d %H:%M")
    elif to_create_time != "":
        param["create_time__lte"] = datetime.datetime.strptime(to_create_time, "%Y-%m-%d %H:%M")
    elif user_mail != "":
        param["user__mail__contains"] = user_mail
    elif user_phone != "":
        param["user__phone__contains"] = user_phone
    elif good_title != "":
        param["orderitem__good__title__contains"] = good_title
    elif good_id != "":
        param["orderitem__good_id"] = int(good_id)

    return Order.objects.filter(**param).distinct().order_by("-id")


@manager_login_required
def order_query(req):
    if req.method == "GET":
        page_num = int(req.GET.get("page_num", 1))
        page_size = int(req.GET.get("page_size", 15))

        p = Paginator(get_query_order(req.GET), page_size)
        page = p.page(page_num)
        order_lst = []
        for order in page.object_list:
            order_lst.append({
                "order_id": order.id,
                "cash": order.cash,
                "status": order.get_status_display(),
                "user": order.user.mail,
                "times": {
                    "create_time": order.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "pay_time": order.pay_time.strftime("%Y-%m-%d %H:%M:%S") if order.pay_time is not None else "暂无",
                    "ship_time": order.ship_time.strftime("%Y-%m-%d %H:%M:%S") if order.ship_time is not None else "暂无"
                },
                "items": [
                    {
                        "good_id": item.good.id,
                        "src": item.good.first_image_url,
                        "title": item.good.title,
                        "price": item.good.price,
                        "size": item.size,
                        "amount": item.amount,
                    } for item in order.order_item
                ]
            })

        return json_response(0, "success", total=p.count, rows=order_lst)


@manager_login_required
def order_export(req):
    if req.method == "POST":
        from .tasks import to_report
        to_report(get_query_order(req.POST), Report.create())
        return json_response(0, "success", redirect="/manager/order/export/")
    elif req.method == "GET":
        return render(req, "order/export.html", context={
            "reports": Report.objects.filter().order_by("-id")
        })


@manager_login_required
def order_export_download(req, report_id):
    try:
        report = Report.objects.get(id=report_id, is_finish=True)
    except Report.DoesNotExist:
        return HttpResponseForbidden
    # 更新下载次数
    Report.objects.filter(id=report_id).update(download_count=F("download_count") + 1)

    response = FileResponse(open(report.get_local_path, 'rb'))
    response['content_type'] = "application/octet-stream"
    response['Content-Disposition'] = 'attachment; filename=' + report.filename
    return response


@manager_login_required
def sell(req):
    if req.method == "GET":
        return render(req, "order/sell.html", context={
            "summit_count": Order.objects.filter(status=Order.SUMMIT).count(),
            "pay_count": Order.objects.filter(status=Order.PAY).count(),
            "ship_count": Order.objects.filter(status=Order.SHIP).count(),
        })


@manager_login_required
def sell_trade_data(req):
    if req.method == "GET":
        from_time = datetime.datetime.strptime(req.GET.get("from_time"), "%Y-%m-%d %H:%M")
        to_time = datetime.datetime.strptime(req.GET.get("to_time"), "%Y-%m-%d %H:%M")
        total_cash = Order.objects.filter(pay_time__gte=from_time, pay_time__lte=to_time).aggregate(
            total_cash=Sum("cash")
        )["total_cash"]
        total_amount = OrderItem.objects.filter(
            order__pay_time__gte=from_time, order__pay_time__lte=to_time
        ).aggregate(
            total_amount=Sum("amount")
        )["total_amount"]
        user_count = Order.objects.filter(
            pay_time__gte=from_time, pay_time__lte=to_time).values('user').distinct().order_by('user').count()
        return json_response(0, "success", data={
            "total_cash": total_cash if total_cash is not None else 0,
            "total_amount": total_amount if total_amount is not None else 0,
            "trade_user_count": user_count,
            "user_price": round(total_cash / user_count, 2) if user_count else 0
        })


@manager_login_required
def sell_good_data(req):
    if req.method == "GET":
        from_time = datetime.datetime.strptime(req.GET.get("from_time"), "%Y-%m-%d %H:%M")
        to_time = datetime.datetime.strptime(req.GET.get("to_time"), "%Y-%m-%d %H:%M")
        user_count = GoodTrack.objects.filter(
            time__gte=from_time, time__lte=to_time).values('user').distinct().order_by('user').count()

        good_visit_count = GoodTrack.objects.filter(
            time__gte=from_time, time__lte=to_time).values('good').distinct().order_by('good').count()

        good_track_count = GoodTrack.objects.filter(time__gte=from_time, time__lte=to_time).count()
        return json_response(0, "success", data={
            "good_visit_count": good_visit_count,
            "good_track_count": good_track_count,
            "good_user_count": user_count,
        })


@manager_login_required
def manager_user(req):
    if req.method == "GET":
        return render(req, "order/manage-user.html")


@manager_login_required
def user_query(req):
    if req.method == "GET":
        page_num = int(req.GET.get("page_num", 1))
        page_size = int(req.GET.get("page_size", 15))

        param = dict()
        mail = req.GET.get("mail", "")
        phone = req.GET.get("phone", "")
        from_create_time = req.GET.get("from_create_time", "")
        to_create_time = req.GET.get("from_create_time", "")

        if mail != "":
            param["mail__contains"] = mail
        elif phone != "":
            param["phone__contains"] = phone
        elif from_create_time != "":
            param["create_time__gte"] = datetime.datetime.strptime(from_create_time, "%Y-%m-%d %H:%M:%S")
        elif to_create_time != "":
            param["create_time__lte"] = datetime.datetime.strptime(to_create_time, "%Y-%m-%d %H:%M:%S")

        objs = User.objects.filter(**param).annotate(
            order_count=Count("order"),
            total_cash=Sum("order__cash")
        ).order_by("id")

        p = Paginator(objs, page_size)
        page = p.page(page_num)
        user_lst = []
        for user in page.object_list:
            user_lst.append({
                "user_id": user.id,
                "total_cash": user.total_cash,
                "order_count": user.order_count,
                "mail": user.mail,
                "phone": user.phone,
                "create_time": user.create_time.strftime("%Y-%m-%d %H:%M:%S"),
                "last_login": user.last_login.strftime("%Y-%m-%d %H:%M:%S")
            })

        return json_response(0, "success", total=p.count, rows=user_lst)


@manager_login_required
def user_track(req, user_id):
    if req.method == "GET":
        # 查询最近七天的浏览记录
        # tracks = GoodTrack.objects.filter(user_id__exact=user_id,
        #                                   time__gte=datetime.datetime.now() - datetime.timedelta(days=7)
        # ).annotate(lastest_time=Max("time")).order_by("-time")

        goods = Good.objects.filter(
            goodtrack__user_id=user_id, goodtrack__time__gte=datetime.datetime.now() - datetime.timedelta(days=7)
        ).annotate(
            last_time=Max("goodtrack__time")
        ).order_by("-last_time")

        # print(goods)
        date_lst = {}
        for good in goods:
            date = good.last_time.strftime("%Y-%m-%d")
            date_lst.setdefault(date, [])
            date_lst[date].append({
                "good_id": good.id,
                "src": good.first_image_url,
                # "time": good.last_time.strftime("%Y-%m-%d %H:%M:%S"),
                "title": good.title
            })

        return json_response(0, "success", data=date_lst)