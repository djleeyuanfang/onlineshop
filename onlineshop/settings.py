"""
Django settings for onlineshop project.

Generated by 'django-admin startproject' using Django 3.0.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'w9aw5z#qlg&th^lf7jog)0g_wew-@m2^kqu^izrnix)avs(w1a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mAuth',
    'order',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'onlineshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'onlineshop.context.collection'
            ],
        },
    },
]

WSGI_APPLICATION = 'onlineshop.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    # os.path.join(BASE_DIR, "MGStudio", "static"),
    os.path.join(BASE_DIR, "static"),
]

# AUTH_USER_MODEL = 'wx.User'

AUTH_USER_MODEL = 'mAuth.User'

LOGIN_URL = '/login/'
AFTER_LOGIN_URL = '/order/'

GOOD_IMAGE_URL = "img/"

GOOD_IMAGE_DIR = "img"
GOOD_IMAGE_ROOT = os.path.join(BASE_DIR, GOOD_IMAGE_DIR)

# 报表文件
EXPORT_DIR = "export"
EXPORT_ROOT = os.path.join(BASE_DIR, EXPORT_DIR)

# 邮箱设置
EMAIL_HOST = 'smtp.163.com'  # 设置SMTP服务器，网易的为 smtp.163.com，其他的以此类推
EMAIL_PORT = 25   # 设置端口，一般都是25
EMAIL_HOST_USER = "djleeyuanfang@163.com"  # 你的邮箱地址
EMAIL_HOST_PASSWORD = "sj9frf7cdis812h"  # 这个时邮箱的授权码，不是登陆密码
EMAIL_SUBJECT_PREFIX = "[DjleeOnlineShop]"  # 邮件标题的前缀
# SERVER_EMAIL = "153*******@qq.com"  # 管理员的邮箱的地址
# 这是在生产环境中，如果发生错误，发送邮件到这个邮箱
# ADMINS = (('153*******', '153*******@qq.com'),)