from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.hello_weight, name='hello_weight'),
    path('home', views.home_func, name='home'),
    path('input/<int:id>', views.input_func, name='input'),
    path('edit_menu', views.edit_func, name='edit_menu'),
    path('result_menu', views.home_func, name="result_menu"),
    path('account', views.account_func, name='account'),
    path('edit/<int:id>', views.edit_menu_func, name='edit'),
    path('delete/<int:id>', views.delete_func, name='delete'),
    path('signup', views.signup_func, name='signup'),
    path('login', views.login_func, name='login'),
    path('logout', views.logout_func, name='logout'),
]
