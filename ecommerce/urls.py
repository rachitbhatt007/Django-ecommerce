from django.urls import path
from . import views


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("product/<slug:slug>", views.ProductDetailView.as_view(),
         name="product_detail"),
    path("cart", views.CartListView.as_view(), name="cart"),
    path("add-to-cart/<slug:slug>", views.AddToCartView.as_view(), name="addtocart"),
    path("remove-from-cart/<slug:slug>",
         views.RemoveFromCartView.as_view(), name="removefromcart"),
    path("checkout", views.CheckoutView.as_view(), name="checkout"),
    path("profile", views.ProfileView.as_view(), name="profile"),
    path("orders", views.OrderView.as_view(), name="orders")
]
