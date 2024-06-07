from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('verify-otp/', views.VerifyOTPView.as_view(), name='verify_otp'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('verify-login-otp/', views.VerifyLoginOTPView.as_view(), name='verify_login_otp'),

    #Team views
    path('team/invite-member/', views.InviteMemberView.as_view(), name='invite_member'),
    path('team/remove-member/', views.RemoveMemberView.as_view(), name='remove_member'),
]