from django.contrib import admin
from django.urls import path
from newapp import views

app_name = 'newapp_in'

urlpatterns = [
path('register/',views.register, name = 'register'),
path('user_login/', views.user_login, name = 'user_login')
]
