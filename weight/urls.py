from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^$', views.home_func, name='home'),
    path('home', views.home_func, name='home'),
    path('input/<int:id>', views.input_func, name='input'),
    path('edit_menu', views.home_func, name='edit_menu'),
    path('regi_menu', views.regi_menu_func, name='regi_menu'),
    path('result_menu', views.home_func, name="result_menu"),
    path('result_list', views.result_list_func, name='result_list'),
    path('result_list_menu/<int:id>', views.result_list_menu_func, name='result_list_menu'),
    path('result_edit/<int:id>', views.result_edit_func, name='result_edit'),
    path('result_delete/<int:id>', views.result_delete_func, name='result_delete'),
    path('result/<int:id>/<str:order_type>/', views.result_func, name="result"),
    path('account', views.account_func, name='account'),
    path('edit/<int:id>', views.menu_edit_func, name='edit'),
    path('delete/<int:id>', views.delete_func, name='delete'),
    path('signup', views.signup_func, name='signup'),
    path('login', views.login_func, name='login'),
    path('logout', views.logout_func, name='logout'),
    path('settings', views.settings_func, name='settings'),
]
