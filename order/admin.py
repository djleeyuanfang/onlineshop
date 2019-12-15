from django.contrib import admin
from .models import *


@admin.register(TestImageUpload)
class TestImageUploadAdmin(admin.ModelAdmin):

    search_fields = ("file_name", )


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("index", "is_show", "label", "name")


@admin.register(Good)
class GoodAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "content", "is_sell")
    search_fields = ("title",)


@admin.register(GoodSize)
class GoodSizeAdmin(admin.ModelAdmin):
    list_display = ("size", "amount", "good")


@admin.register(GoodImage)
class GoodImageAdmin(admin.ModelAdmin):
    list_display = ("index", "good")


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "file_name", "img", "image_dir")


@admin.register(ImageDir)
class ImageDirAdmin(admin.ModelAdmin):
    list_display = ("id", "direction")


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", )


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("amount", "size", "good", "cart")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "cash", "status", "user", "create_time", "pay_time")

    list_editable = ("status", )


@admin.register(GoodTrack)
class GoodTrackAdmin(admin.ModelAdmin):
    list_display = ("good", "user", "time")