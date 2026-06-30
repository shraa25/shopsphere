from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cart, CartItem
from products.models import Product
from django.views.generic import ListView
from products.models import Product

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



class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 8

    def get_queryset(self):

        queryset = Product.objects.filter(
            is_available=True
        )

        search = self.request.GET.get("search")

        category = self.request.GET.get("category")

        sort = self.request.GET.get("sort")

        if search:
            queryset = queryset.filter(
                name__icontains=search
            )

        if category:
            queryset = queryset.filter(
                category_id=category
            )

        if sort == "low":
            queryset = queryset.order_by("price")

        elif sort == "high":
            queryset = queryset.order_by("-price")

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all()

        return context