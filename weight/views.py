from django.shortcuts import render
from django.http.response import HttpResponse
from django.db.models import Max
from .models import Menu, Record
from .forms import RecordForm

# Create your views here.

def hello_weight(request):
    return render(request, 'index.html')

def hello_home(request):
    menu_list = Menu.objects.all().order_by('id')
    return render(request, 'home.html', {'menu_list':menu_list})

def input_func(request, id):
    
    if request.method == 'POST':
        form = RecordForm(request.POST or None)
        if form.is_valid():
            register_record = Record()

            register_record.weight_record = form.cleaned_data['weight_record']

            Record.objects.create(
                weight_menu = Menu(id = id),
                weight_record = register_record.weight_record,
            )

            latest_rec = Record.objects.filter(weight_menu__id= id).latest('created_at')
            max_rec = Record.objects.filter(weight_menu__id= id).order_by('weight_record').last()

    else:
        #外部キーの値を取得する時は定義した外部キーの項目名にアンダーバーを２つ続けて、取得したいデータの値を指定する。
        latest_rec = Record.objects.filter(weight_menu__id= id).latest('created_at')
        max_rec = Record.objects.filter(weight_menu__id= id).order_by('weight_record').last()
        #getの時は、空のフォームを作成してレンダリング
        form = RecordForm()
    return render(request, 'input.html', {'id':id, 'latest_rec':latest_rec, 'max_rec':max_rec, 'form':form})