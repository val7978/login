from django.urls import path
from .views import (
    home_view,
    login_view,
    register_view,
    logout_view,
    dashboard_view,
    register_work_view,
    password_reset_request_view,
    password_reset_confirm_view,
)

urlpatterns = [
    path('', home_view, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('register-work/', register_work_view, name='register_work'),
    path('reset-password/', password_reset_request_view, name='password_reset_request'),
    path('reset-password/<str:token>/', password_reset_confirm_view, name='password_reset_confirm'),
]