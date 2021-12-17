from django.contrib import admin
from django.urls import path, include
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('register/', user_register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('blog/', blog, name='blog'),
    path('add_blog/', add_blog, name='add_blog'),
    path('blog_details/<str:slug>', blog_details, name='blog_details'),
    path('see_blog/', see_blog, name='see_blog'),
    path('blog_delete/<int:id>', blog_delete, name='blog_delete'),
    path('blog_update/<str:slug>/', blog_update, name='blog_update'),
] 