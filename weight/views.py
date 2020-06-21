from django.shortcuts import render
from django.http.response import HttpResponse
from .models import Menu, Record

# Create your views here.

def hello_weight(request):
    return render(request, 'index.html')

def hello_home(request):
    menu_list = Menu.objects.all().order_by('id')
    return render(request, 'home.html', {'menu_list':menu_list})

def input_func(request, id):
    return render(request, 'input.html', {'id':id})