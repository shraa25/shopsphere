from django.views.generic import ListView, DetailView
from .models import Product, Category
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .models import Wishlist
from django.contrib.auth.mixins import LoginRequiredMixin

class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 8

    def get_queryset(self):

        queryset = Product.objects.filter(is_available=True)

        search = self.request.GET.get("search")
        category = self.request.GET.get("category")
        sort = self.request.GET.get("sort")

        if search:
            queryset = queryset.filter(name__icontains=search)

        if category:
            queryset = queryset.filter(category_id=category)

        if sort == "low":
            queryset = queryset.order_by("price")

        elif sort == "high":
            queryset = queryset.order_by("-price")

        return queryset

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["categories"] = Category.objects.all()

        return context


class ProductDetailView(DetailView):

    model = Product

    template_name = "products/product_detail.html"

    context_object_name = "product"

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:

            context["in_wishlist"] = Wishlist.objects.filter(

                user=self.request.user,

                product=self.object

            ).exists()

        return context
@login_required
def add_to_wishlist(request, pk):

    product = Product.objects.get(pk=pk)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect("product_detail", pk=pk)


class WishlistView(LoginRequiredMixin, ListView):

    model = Wishlist

    template_name = "products/wishlist.html"

    context_object_name = "wishlist"

    def get_queryset(self):

        return Wishlist.objects.filter(
            user=self.request.user
        )

@login_required
def remove_from_wishlist(request, pk):

    Wishlist.objects.filter(
        user=request.user,
        product_id=pk
    ).delete() 

    return redirect("product_detail", pk=pk)

def get_context_data(self, **kwargs):

    context = super().get_context_data(**kwargs)

    context["categories"] = Category.objects.all()

    if self.request.user.is_authenticated:
        context["wishlist_count"] = Wishlist.objects.filter(
            user=self.request.user
        ).count()
    else:
        context["wishlist_count"] = 0

    return context