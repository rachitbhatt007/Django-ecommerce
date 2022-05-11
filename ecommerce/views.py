from django.shortcuts import render, redirect, reverse

from django.views import View
from django.views.generic import ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import AddToCartForm, CheckoutForm
from .models import *
from account.models import UserProfile, Address

from django.contrib import messages
from django.utils import timezone

from django.core.paginator import Paginator
from django.core.mail import send_mail
# Create your views here.


class IndexView(View):
    def get(self, request):
        products = Product.objects.all().order_by("id")
        search_item = request.GET.get("search")
        if search_item:
            search_item = request.GET.get("search")
            products = Product.objects.filter(name__icontains=search_item)
           

        sort_param = request.GET.get("sort")
        if(sort_param == "product_name"):
            products = products.order_by('name')
            paginator = Paginator(products, 4)
        elif(sort_param == "price_asc"):
            products = products.order_by('price')
            paginator = Paginator(products, 4)
        elif(sort_param == "price_des"):
            products = products.order_by('-price')
            paginator = Paginator(products, 4)

        paginator = Paginator(products, 4)
        page = request.GET.get("page")
        products = paginator.get_page(page)
        total_pages_str = "a"*products.paginator.num_pages
        context = {
            "products": products,
            "sort_param": sort_param,
            "total_pages": total_pages_str,
            "search_item": search_item}
        return render(request, "ecommerce/homepage.html", context)

        # paginator = Paginator(products, 4)
        # page = request.GET.get("page")
        # products = paginator.get_page(page)
        # total_pages_str = "a"*products.paginator.num_pages
        # context = {
        #     "products": products,
        #     "total_pages":total_pages_str}
        # return render(request, "ecommerce/homepage.html", context)


class ProductDetailView(View):
    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        form = AddToCartForm(initial={"cart_quantity": 1})
        context = {
            "form": form,
            "product": product
        }
        return render(request, "ecommerce/product_detail.html", context)


class CartListView(LoginRequiredMixin, ListView):
    login_url = "login"
    template_name = "ecommerce/cartpage.html"
    model = OrderItem

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if OrderItem.objects.filter(
                user__user__username=self.request.user.username, ordered=False).exists():
            order_items = OrderItem.objects.filter(
                user__user__username=self.request.user.username, ordered=False)
        else:
            order_items = None
        if Order.objects.filter(user__user__username=self.request.user.username, ordered=False).exists():
            order = Order.objects.get(
                user__user__username=self.request.user.username, ordered=False)
        else:
            order = None
        context["order_items"] = order_items
        context["order"] = order
        return context


class CheckoutView(View):
    def get(self, request):
        user = UserProfile.objects.get(user__username=request.user.username)
        order_items = OrderItem.objects.filter(
            user__user__username=self.request.user.username, ordered=False)
        if Order.objects.filter(user__user__username=self.request.user.username, ordered=False).exists():
            order = Order.objects.filter(
                user__user__username=self.request.user.username, ordered=False)[0]
        else:
            order = None
        form_data = {
            "name": user.user.username,
            "address": Address.objects.get(default=True, user__user__username=request.user.username),
            "email": user.user.email
        }
        form = CheckoutForm(initial=form_data)
        context = {
            "order_items": order_items,
            "order": order,
            "form": form
        }
        return render(request, "ecommerce/checkoutpage.html", context)

    def post(self, request):
        user = UserProfile.objects.get(user__username=request.user.username)
        form = CheckoutForm(request.POST)
        if(form.is_valid()):
            if Order.objects.filter(user__user__username=self.request.user.username, ordered=False).exists():
                ordered_date = timezone.now()
                order = Order.objects.get(
                    user__user__username=self.request.user.username, ordered=False)
                for order_item in order.items.all():
                    order_item.product.quantity -= order_item.quantity
                    order_item.product.save()
                order.items.all().update(ordered=True)
                order.ordered = True
                order.order_date = ordered_date
                order.save()
                context = {
                    "order_id": order.id
                }
                send_mail(
                    "Your order has been placed",
                    f"Thanks for ordering from Ecom. your order Id is {order.id}.Your order will be delivered soon\nwarm regards\nEcom",
                    "rachit.bhatt@gmail.com",
                    [f'{order.user.user.email}'],
                )
                return render(request, "ecommerce/thankyou.html", context)
            else:
                messages.info(
                    request, "Please add items to the cart to place an order")
                return redirect(reverse("index"))
        else:
            messages.info(request, f"Please fill all the fields")
            return redirect(reverse("checkout"))


class AddToCartView(LoginRequiredMixin, View):
    login_url = 'login'

    def post(self, request, slug):
        product = Product.objects.get(slug=slug)
        user = UserProfile.objects.get(user__username=request.user.username)
        order_item, created = OrderItem.objects.get_or_create(
            product=product, user=user, ordered=False)

        cart_quantity = 0
        if(request.POST.get("cart_quantity") is not None):
            cart_quantity = request.POST.get("cart_quantity")
            cart_quantity = int(cart_quantity)

            if product.quantity < cart_quantity and order_item.quantity+cart_quantity > product.quantity:
                messages.info(
                    request, f"Only {product.quantity} of these items are left")
                return redirect(reverse("product_detail", args=(slug,)))
            elif cart_quantity <= 0:
                messages.info(
                    request, f"cart_quantity cannot be negative or zero")
                return redirect(reverse("product_detail", args=(slug,)))

        # adding quantity to zero
        if(created and cart_quantity > 0):
            order_item.quantity = cart_quantity
            order_item.save()
        elif(created and cart_quantity == 0):
            order_item.quantity = 1
            order_item.save()

        # adding quantity to already added products
        order_qs = Order.objects.filter(
            user__user__username=request.user.username, ordered=False)

        if(order_qs.exists()):
            order = order_qs[0]
            if order.items.filter(product__slug=product.slug).exists() and order_item.quantity+cart_quantity <= product.quantity and cart_quantity != 0:
                order_item.quantity += int(cart_quantity)
                order_item.save()
                messages.info(request, f"Item quantity is update")
            elif order.items.filter(product__slug=product.slug).exists() and order_item.quantity+cart_quantity > product.quantity:
                messages.info(
                    request, f"You can add only {product.quantity - order_item.quantity} more items")
            elif order.items.filter(product__slug=product.slug).exists() and not created and order_item.quantity+cart_quantity < product.quantity:
                order_item.quantity += (cart_quantity)+1
                order_item.save()
                messages.info(request, f"Item quantity is updated")

            elif order.items.filter(product__slug=product.slug).exists() and not created and order_item.quantity+cart_quantity == product.quantity:
                messages.info(
                    request, f"You have already added the max quantity available")
            else:
                messages.info(request, "Item added to cart")
                order.items.add(order_item)

        else:
            order = Order.objects.create(user=user)
            order.items.add(order_item)
            messages.info(request, "Item added to the cart")

        if(cart_quantity == 0):
            return redirect(reverse("index"))
        else:
            return redirect(reverse("product_detail", args=(slug,)))


class RemoveFromCartView(LoginRequiredMixin, View):
    login_url = "login"
    # Remove from cart

    def get(self, request, slug):
        product = Product.objects.get(slug=slug)
        user = UserProfile.objects.get(user__username=request.user.username)
        order_qs = Order.objects.filter(
            user__user__username=request.user.username, ordered=False)

        if(order_qs.exists()):
            order = order_qs[0]
            if order.items.filter(product__slug=product.slug).exists():
                order_item = OrderItem.objects.get(
                    product=product, user=user, ordered=False)

                order.items.remove(order_item)
                order_item.delete()

                messages.info(request, f"Item has been removed")

                return redirect(reverse("cart"))

            else:
                return redirect(reverse("cart"))
    # remove one item from cart

    def post(self, request, slug):
        product = Product.objects.get(slug=slug)
        user = UserProfile.objects.get(user__username=request.user.username)
        orderitem = OrderItem.objects.get(
            user__user=request.user, product=product, ordered=False)
        if(orderitem.quantity == 1):
            return redirect(reverse("removefromcart", args=(slug,)))
        else:
            orderitem.quantity -= 1
            orderitem.save()
            return redirect(reverse("cart"))


class ProfileView(View):
    def get(self, request):
        context = {
            "addresses": Address.objects.filter(user__user__username=request.user.username)
        }
        return render(request, "ecommerce/user_profile.html", context)

# changing default address
    def post(self, request):
        address_id = request.POST.get("address")
        address = Address.objects.get(
            user__user__username=request.user.username, id=address_id)
        default_address = Address.objects.get(
            user__user__username=request.user.username, default=True)
        default_address.default = False
        address.default = True
        default_address.save()
        address.save()

        return redirect(reverse("profile"))


class OrderView(ListView):
    template_name = "ecommerce/orders.html"
    model = Order
    context_object_name = "orders"

    def get_queryset(self):
        base_query = super().get_queryset()
        orderitems_query = base_query.filter(
            user__user__username=self.request.user.username, ordered=True).order_by('-id')
        return orderitems_query
