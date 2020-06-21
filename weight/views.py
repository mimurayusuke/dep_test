from django.shortcuts import render
from django.http.response import HttpResponse
from django.db.models import Max
from .models import Menu, Record

# Create your views here.

def hello_weight(request):
    return render(request, 'index.html')

def hello_home(request):
    menu_list = Menu.objects.all().order_by('id')
    return render(request, 'home.html', {'menu_list':menu_list})

def input_func(request, id):
    #外部キーの値を取得する時は定義した外部キーの項目名にアンダーバーを２つ続けて、取得したいデータの値を指定する。
    latest_rec = Record.objects.filter(weight_menu__id= id).latest('created_at')
    max_rec = Record.objects.filter(weight_menu__id= id).order_by('weight_record').last()
    return render(request, 'input.html', {'id':id, 'latest_rec':latest_rec, 'max_rec':max_rec})