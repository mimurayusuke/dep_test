from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.hello_weight, name='hello_weight'),
    path('home', views.hello_home, name='hello_home')
]