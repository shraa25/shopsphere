from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from cart.models import Cart
from .models import Order, OrderItem


@login_required
def checkout(request):

    cart = Cart.objects.get(user=request.user)

    if cart.items.count() == 0:
        return redirect("cart")

    if request.method == "POST":

        order = Order.objects.create(
            user=request.user,
            total=cart.total
        )

        for item in cart.items.all():

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart.items.all().delete()

        return redirect("order_success")

    return render(
        request,
        "orders/checkout.html",
        {"cart": cart}
    )

@login_required
def order_success(request):

    return render(
        request,
        "orders/order_success.html"
    )