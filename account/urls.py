from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("login", views.LoginView.as_view(), name="login"),
    path("logout", views.LogoutView.as_view(), name="logout"),
    path("register", views.RegisterView.as_view(), name="register"),


    path('password_reset/', auth_views.PasswordResetView.as_view(template_name="account/password_reset.html"),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html"),
         name='password_reset_complete'),
]
