from django.urls import path
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),  
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name="register"),
    path('logout/', views.logout_view, name='logout'),
]