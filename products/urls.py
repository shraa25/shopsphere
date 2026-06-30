from django.urls import path
from .views import ProductListView, ProductDetailView
from . import views
urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),

    path("<int:pk>/", ProductDetailView.as_view(), name="product_detail"),
    path(
    "<int:pk>/wishlist/",
    views.add_to_wishlist,
    name="add_to_wishlist",
),

path(
    "wishlist/",
    views.WishlistView.as_view(),
    name="wishlist",
),

path(
    "wishlist/remove/<int:pk>/",
    views.remove_from_wishlist,
    name="remove_from_wishlist",
),
]