from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings

from .models import User, MailCode


def json_response(code, msg, **kwargs):
    res = {
        'code': code,
        'msg': msg,
    }
    res.update(kwargs)
    return JsonResponse(res)


@csrf_exempt
def login(req):
    if req.method == "GET":
        return render(req, "mAuth/customer_login.html")
    elif req.method == "POST":
        mail = req.POST.get("mail", "")
        passwd = req.POST.get("passwd", "")
        user = auth.authenticate(username=mail, password=passwd)
        if user:
            auth.login(req, user)
            return json_response(0, "登录成功", redirect=settings.AFTER_LOGIN_URL)
        else:
            return json_response(1, "账号或密码错误")


@csrf_exempt
def register(req):
    if req.method == "GET":
        return render(req, "mAuth/customer_register.html")
    elif req.method == "POST":
        mail = req.POST.get("mail", "")
        mail_code = req.POST.get("mail_code", "")
        print("mail", mail, "mail_code", mail_code)
        if MailCode.check_mail_code(mail, mail_code):
            phone = req.POST.get("phone", "")
            passwd = req.POST.get("passwd", "")
            try:
                user = User.objects.get(mail=mail)
                user.password = passwd
                user.phone = phone
                user.save()
                return json_response(0, "修改密码成功", redirect="/login/")
            except User.DoesNotExist:
                User.objects.create_user(mail, passwd, phone)
                return json_response(0, "注册成功", redirect="/login/")
        return json_response(1, "验证码错误")


@csrf_exempt
def logout(req):
    if req.method == "GET":
        auth.logout(req)
        return redirect("/login/")


@csrf_exempt
def send_mail_code(req):
    if MailCode.send_mail_code(req.POST.get("mail", "")):
        return json_response(0, "发送成功")
    else:
        return json_response(1, "发送频繁，请稍后重试")
