from django.shortcuts import render, redirect, reverse
from django.http import Http404
from .models import *
from .forms import UserRegisterForm, UserRegisterForm2, UserLoginForm
from django.contrib.auth.models import User
from django.views import View
from django.views.generic.base import TemplateView
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.


class LoginView(View):
    def get(self, request):
        form = UserLoginForm()
        context = {"form": form}
        return render(request, "account/login.html", context)

    def post(self, request):
        form = UserLoginForm(request.POST)
        email = request.POST.get("email")
        try:
            username = User.objects.get(email=email).username
        except:
            messages.info(request, f"Invalid username or password")
            return redirect(reverse("login"))
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if(user is not None):
            login(request, user)
            return redirect(reverse("index"))
        else:

            messages.info(request, f"Invalid username or password")
            return redirect(reverse("login"))


class RegisterView(View):

    def get(self, request):
        form = UserRegisterForm()
        form2 = UserRegisterForm2()
        context = {"form": form,
                   "form2": form2}
        return render(request, "account/register.html", context)

    def post(self, request):
        form = UserRegisterForm(request.POST)
        form2 = UserRegisterForm2(request.POST)
        if form.is_valid() and form2.is_valid():
            user = form.save(commit=False)
            user.email = request.POST.get("email")
            form.save()
            userprofile = form2.save(commit=False)
            username = form.cleaned_data["username"]
            address = form2.cleaned_data["address"]
            userprofile.user = User.objects.get(username=username)
            form2.save()
            user_address = Address(
                user=userprofile, default=True, user_address=address)
            user_address.save()
            userprofile.address = user_address
            userprofile.save()

            messages.success(
                request, f"Congratulations!! Your account has been created")
            send_mail(
                "Welcome to Ecom family",
                "Thanks for registering to Ecom.\nwarm regards\nEcom",
                settings.EMAIL_HOST_USER,
                [f'{user.email}'],
            )
            return redirect(reverse("index"))
        else:
            context = {"form": form,
                       "form2": form2}
            return render(request, "account/register.html", context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse("login"))
