from django.urls import path
from . import views

urlpatterns = [

    path(
        "checkout/",
        views.checkout,
        name="checkout"
    ),

    path(
        "success/",
        views.order_success,
        name="order_success"
    ),

    path(
    "",
    views.OrderListView.as_view(),
    name="order_list"
),

path(
    "<int:pk>/",
    views.OrderDetailView.as_view(),
    name="order_detail"
),

]