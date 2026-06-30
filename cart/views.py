from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Cart, CartItem
from products.models import Product


class CartView(LoginRequiredMixin, TemplateView):
    template_name = "cart/cart.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cart, created = Cart.objects.get_or_create(
            user=self.request.user
        )

        context["cart"] = cart
        context["items"] = cart.items.all()

        return context


def add_to_cart(request, pk):

    if not request.user.is_authenticated:
        return redirect("login")

    product = Product.objects.get(pk=pk)

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    return redirect("cart")

def increase_quantity(request, pk):

    item = CartItem.objects.get(pk=pk)

    item.quantity += 1

    item.save()

    return redirect("cart")
def decrease_quantity(request, pk):

    item = CartItem.objects.get(pk=pk)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect("cart")
def remove_item(request, pk):

    item = CartItem.objects.get(pk=pk)

    item.delete()

    return redirect("cart")