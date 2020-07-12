from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.home_func, name='home'),
    path('home', views.home_func, name='home'),
    path('input/<int:id>', views.input_func, name='input'),
    path('edit_menu', views.edit_menu_func, name='edit_menu'),
    path('result_menu', views.home_func, name="result_menu"),
    path('result/<int:id>/<str:order_type>/', views.result_func, name="result"),
    path('account', views.account_func, name='account'),
    path('edit/<int:id>', views.edit_func, name='edit'),
    path('delete/<int:id>', views.delete_func, name='delete'),
    path('signup', views.signup_func, name='signup'),
    path('login', views.login_func, name='login'),
    path('logout', views.logout_func, name='logout'),
]
