from django.urls import path
from .views import CartView, add_to_cart
from django.urls import path
from . import views

urlpatterns = [
    path("", CartView.as_view(), name="cart"),
    path("add/<int:pk>/", add_to_cart, name="add_to_cart"),

    path(
        "increase/<int:pk>/",
        views.increase_quantity,
        name="increase_quantity"
),

path(
    "decrease/<int:pk>/",
    views.decrease_quantity,
    name="decrease_quantity"
),

path(
    "remove/<int:pk>/",
    views.remove_item,
    name="remove_item"
),
]