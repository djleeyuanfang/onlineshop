from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path("", views.collection),
    path("collection/<label>/", views.collection),
    path("good/<good_id>/", views.view_good),
    path("good/<good_id>/add_cart", views.add_cart),
    path("cart/", views.get_cart),
    path("cart/change/", views.update_cart),
    path("cart/submit/", views.cart_submit),
    path("order/<order_id>/", views.order_detail),
    path("order/<order_id>/<op>/", views.order_operation),
    path("order/", views.my_order),
    path("upload_image/", views.upload_image),
    path("images/", views.get_images),
    path("upload_img/", views.upload_image),
    path("manager/goods/", views.good_lst_page),
    path("manager/goods/query/", views.good_lst),
    path("manager/add_good/", views.add_good),
    path("manager/good/", views.edit_goods),
    path("manager/good/<good_id>/", views.manager_good),
    path("manager/good/<good_id>/save/", views.update_good),
    path("manager/good/<good_id>/down/", views.down_good),
    path("manager/good/<good_id>/remove/", views.remove_good),
    path("manager/collection/", views.manager_collection),
    path("manager/order/", views.manager_order),
    path("manager/order/query/", views.order_query),
    path("manager/order/export/", views.order_export),
    path("manager/order/export/<report_id>/", views.order_export_download),
    path("manager/sell/", views.sell),
    path("manager/sell/trade/", views.sell_trade_data),
    path("manager/sell/good/", views.sell_good_data),
    path("manager/user/", views.manager_user),
    path("manager/user/query/", views.user_query),
    path("manager/user/<user_id>/track/", views.user_track),
]
