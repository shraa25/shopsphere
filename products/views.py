from django.views.generic import ListView, DetailView
from .models import Product, Category


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