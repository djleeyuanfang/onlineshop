import datetime
import os
import random

from django.db import models
from django.conf import settings
import uuid


class Collection(models.Model):
    label = models.CharField(max_length=30, verbose_name="英文标签", unique=True)
    name = models.CharField(max_length=30, verbose_name="描述", unique=True)
    index = models.SmallIntegerField(verbose_name="顺序")

    is_show = models.BooleanField(default=True, verbose_name="显示在面板上面")

    class Meta:
        verbose_name = "商品分类"


class Good(models.Model):
    title = models.CharField(default="未定义标题", max_length=100, verbose_name="标题")
    price = models.FloatField(default=0, verbose_name="价格")

    content = models.CharField(default="<ul><li>未定义内容</li></ul>", max_length=200, verbose_name="商品说明")

    collections = models.ManyToManyField("Collection")

    # is_edit = models.BooleanField(default=True, verbose_name="草稿")
    is_sell = models.BooleanField(default=False, verbose_name="在售")

    @property
    def images(self):
        return self.goodimage_set.order_by("index")

    @property
    def first_image_url(self):
        images = self.goodimage_set.order_by("index")
        if images:
            return images[0].image.img.url
        else:
            return "{}/none.png".format(settings.GOOD_IMAGE_DIR)

    @property
    def sizes(self):
        return self.goodsize_set.order_by("index")

    def to_first_view(self):
        return {
            "id": self.id,
            "title": self.title,
            "price": self.price,
            "first_image_url": self.first_image_url
        }

    class Meta:
        verbose_name = "商品"


class GoodTrack(models.Model):
    good = models.ForeignKey(Good, on_delete=models.DO_NOTHING, verbose_name="商品")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name="用户")
    time = models.DateTimeField(auto_now=True, verbose_name="记录时间")

    class Meta:
        verbose_name = "浏览足迹"


class GoodSize(models.Model):
    index = models.SmallIntegerField(verbose_name="序号")
    size = models.CharField(max_length=5, verbose_name="码数")
    amount = models.PositiveIntegerField(default=0, verbose_name="存量")

    good = models.ForeignKey(Good, on_delete=models.DO_NOTHING, verbose_name="商品")


def dre_path(instance, filename):
    return "{}/{}.png".format(settings.GOOD_IMAGE_DIR, uuid.uuid4().hex)


class TestImageUpload(models.Model):
    file_name = models.CharField(max_length=32, verbose_name="上传文件名")
    img = models.ImageField(upload_to=dre_path)


class ImageDir(models.Model):
    direction = models.CharField(max_length=50, verbose_name="分类目录", unique=True)

    def __str__(self):
        return self.direction


class Image(models.Model):
    file_name = models.CharField(max_length=32, verbose_name="上传文件名")
    img = models.ImageField(upload_to=dre_path)

    image_dir = models.ForeignKey(ImageDir, on_delete=models.DO_NOTHING, verbose_name="目录", null=True)

    def to_json(self):
        return {
            "id": self.id,
            "url": self.img.url,
            "file_name": self.file_name
        }


class GoodImage(models.Model):
    # filename = models.CharField(max_length=32, verbose_name="上传原始文件名")
    image = models.ForeignKey(Image, on_delete=models.DO_NOTHING, verbose_name="图片", null=True)
    index = models.SmallIntegerField(verbose_name="序号")

    good = models.ForeignKey(Good, on_delete=models.DO_NOTHING, verbose_name="商品")

    class Meta:
        verbose_name = "商品图片"


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name="用户")

    @property
    def items(self):
        return self.cartitem_set.all()

    class Meta:
        verbose_name = "购物车"


class CartItem(models.Model):
    amount = models.PositiveIntegerField(verbose_name="数量")
    size = models.CharField(max_length=4, verbose_name="码数")

    good = models.ForeignKey(Good, on_delete=models.DO_NOTHING, verbose_name="商品")

    cart = models.ForeignKey(Cart, on_delete=models.DO_NOTHING, verbose_name="购物车")

    def to_order_item(self):
        return OrderItem(amount=self.amount, size=self.size, good=self.good)

    class Meta:
        verbose_name = "购物车项目"


class Order(models.Model):
    cash = models.FloatField(verbose_name="总价")

    # 订单状态
    SUMMIT = "SUMMIT"
    PAY = "PAY"
    SHIP = "SHIP"
    COMPLETE = "COMPLETE"
    CANCEL = "CANCEL"
    STATUS_CHOICES = (
        (SUMMIT, "订单已提交，待付款"),
        (PAY, "订单已付款，待发货"),
        (SHIP, "订单运送中，待收货"),
        (COMPLETE, "订单完成"),
        (CANCEL, "交易关闭"),
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=SUMMIT, verbose_name="订单状态")

    address = models.CharField(max_length=100, verbose_name="地址")
    express_number = models.CharField(default="暂无", max_length=32, verbose_name="快递单号")
    express_cmp = models.CharField(default="暂无", max_length=32, verbose_name="快递公司")

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name="用户")

    create_time = models.DateTimeField(auto_now_add=True, verbose_name="订单创建时间")
    pay_time = models.DateTimeField(null=True, verbose_name="订单付款时间")
    ship_time = models.DateTimeField(null=True, verbose_name="订单发货时间")
    complete_time = models.DateTimeField(null=True, verbose_name="订单成交时间")

    @property
    def order_item(self):
        return self.orderitem_set.all()

    class Meta:
        verbose_name = "订单"


class OrderItem(models.Model):
    amount = models.PositiveIntegerField(verbose_name="数量")
    size = models.CharField(max_length=4, verbose_name="码数")

    good = models.ForeignKey(Good, on_delete=models.DO_NOTHING, verbose_name="商品")

    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING, verbose_name="订单")

    class Meta:
        verbose_name = "订单项目"


class Report(models.Model):
    filename = models.CharField(max_length=128, verbose_name="文件名路径", unique=True)
    count = models.PositiveIntegerField(default=0, verbose_name="订单条数")
    download_count = models.PositiveIntegerField(default=0, verbose_name="下载次数")
    is_finish = models.BooleanField(default=False, verbose_name="是否生成")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="生成时间")

    class Meta:
        verbose_name = "订单报表"

    @property
    def get_local_path(self):
        return os.path.join(settings.EXPORT_ROOT, self.filename)

    @staticmethod
    def create():
        filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "%s.xls" % random.randint(1000, 9999)
        return Report.objects.create(filename=filename)
