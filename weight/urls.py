from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.hello_weight, name='hello_weight'),
    path('home', views.hello_home, name='hello_home'),
    path('input/<int:id>', views.input_func, name='input'),
    path('edit_menu', views.edit_func, name='edit'),
    path('edit/<int:id>', views.edit_menu_func, name='edit_menu'),
    path('delete/<int:id>', views.delete_func, name='delete'),
    path('signup', views.signup_func, name='signup'),
    path('logout', views.logout_func, name='logout'),
]
