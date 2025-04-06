from django.urls import path
from . import views


urlpatterns = [
    #path('register/', views.registerPage, name='register'),  # ✅ Now correctly linked to views.py
    path('register/', views.RegisterView, name='register'),
    path('login/', views.LoginView, name='login'),
    path('logout/', views.LogoutView, name='logout'),
    path('forgot-password/', views.ForgotPassword, name='forgot-password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.ResetPassword, name='reset-password'),
    path('profile/', views.profile, name='profile'),
    path('coordinator_login/', views.coordinator_view, name='coordinator_login'),
    path('coordinator_dashboard/', views.coordinator_dashboard, name='coordinator_dashboard'),
    #path('coordinator_dashboard_dept/', views.coordinator_dash_dept, name='coordinator_dashboard_dept'),



]
    
