from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
import datetime
import random

from django.core.mail import send_mail


class UserManager(BaseUserManager):
    def create_user(self, mail, passwd, phone=""):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not mail or not passwd:
            raise ValueError('Users must have an openid')

        user = self.model(
            mail=mail,
            phone=phone
        )
        user.set_password(passwd)
        user.save(using=self._db)
        return user

    def update_user_phone(self, mail, phone=""):
        if len(phone) != 11:
            return False

        users = User.objects.filter(mail=mail)
        if users:
            user = users[0]
            user.save(using=self._db)
            return user

    def create_superuser(self, mail, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.model(
            mail=mail,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    mail = models.CharField(max_length=50, unique=True, verbose_name='邮箱')
    phone = models.CharField(max_length=11, verbose_name='手机号', default="")
    is_active = models.BooleanField(default=True, verbose_name='有效')
    is_admin = models.BooleanField(default=False, verbose_name='管理员')

    last_login = models.DateTimeField(verbose_name='上次登录', null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='注册时间')

    objects = UserManager()

    USERNAME_FIELD = 'mail'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "用户"

    def get_full_name(self):
        # The user is identified by their email address
        return self.mail

    def get_short_name(self):
        # The user is identified by their email address
        return self.mail

    def __str__(self):              # __unicode__ on Python 2
        return self.mail

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class MailCode(models.Model):
    mail = models.CharField(max_length=50, unique=True, verbose_name='邮箱')
    code = models.CharField(max_length=6, verbose_name='验证码')
    create_time = models.DateTimeField(auto_now=True, verbose_name="验证码时间")

    class Meta:
        verbose_name = "邮箱验证码"

    @staticmethod
    def check_mail_code(mail, code):
        # 15分钟有效
        limit_time = datetime.datetime.now() - datetime.timedelta(minutes=15)
        return MailCode.objects.filter(mail=mail, code=code, create_time__gte=limit_time).exists()

    @staticmethod
    def send_mail_code(mail):
        # 至少间隔1分钟发一次
        limit_time = datetime.datetime.now() - datetime.timedelta(minutes=1)

        try:
            mail_code = MailCode.objects.get(mail=mail)
            if mail_code.create_time > limit_time:
                return False
        except MailCode.DoesNotExist:
            mail_code = MailCode(mail=mail)
        code = str(random.randint(0, 999999)).rjust(6, "0")
        mail_code.code = code
        try:
            send_mail("[DjleeOnlineShop]安全验证码", "邮箱验证码：%s\n15分钟内有效。" % code, settings.EMAIL_HOST_USER, [mail])
        except Exception as e:
            return False
        mail_code.save()
        return True
