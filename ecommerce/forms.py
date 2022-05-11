from django import forms
from account.models import UserProfile


class AddToCartForm(forms.Form):
    cart_quantity = forms.IntegerField()


class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=50)
    email = forms.EmailField()
    address = forms.CharField(widget=forms.Textarea())
    postal_code = forms.CharField(max_length=8)
    city = forms.CharField(max_length=50)
