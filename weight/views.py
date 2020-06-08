from django.shortcuts import render
from django.http.response import HttpResponse

# Create your views here.

def hello_weight(request):
    return render(request, 'index.html')