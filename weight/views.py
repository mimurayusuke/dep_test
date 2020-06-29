from django.shortcuts import render, redirect, Http404
from django.http.response import HttpResponse
from django.db.models import Max
from .models import Menu, Record
from .forms import RecordForm, MenuForm

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
            return redirect('input', id)

    else:
        #外部キーの値を取得する時は定義した外部キーの項目名にアンダーバーを２つ続けて、取得したいデータの値を指定する。
        latest_rec = Record.objects.filter(weight_menu__id= id).latest('created_at')
        max_rec = Record.objects.filter(weight_menu__id= id).order_by('weight_record').last()
        #getの時は、空のフォームを作成してレンダリング
        form = RecordForm()
    return render(request, 'input.html', {'id':id, 'latest_rec':latest_rec, 'max_rec':max_rec, 'form':form})

def edit_func(request):
    
    if request.method == 'POST':
        form = MenuForm(request.POST or None)
        if form.is_valid():
            register_menu = Menu()
            register_menu.menu_name = form.cleaned_data['menu_name']

            #登録するメニューが既に存在する場合はエラーメッセージを返し、存在しない時に登録する。
            if  Menu.objects.filter(menu_name = register_menu.menu_name).exists():
                error_message = "は既に登録されています。"
                form = MenuForm()
                menu_list = Menu.objects.all().order_by('id')
                return render(request, 'edit.html', {'menu_list':menu_list, 'form':form, 'error_message':error_message, 'registered_menu':register_menu.menu_name})
            else:
                Menu.objects.create(
                    menu_name = register_menu.menu_name,
                )
                #新規登録したメニューの記録を0kgで作成する。
                #この処理がない場合、home画面で新規登録したメニューをクリックした際に、レコードを探してこれない
                #ためエラーとなる。
                new_menu_id = Menu.objects.get(menu_name = register_menu.menu_name)
                print(new_menu_id.id)
                Record.objects.create(
                weight_menu = Menu(id = new_menu_id.id),
                weight_record = 0.00,
            )

            return redirect('edit')

    else:
        form = MenuForm()
        menu_list = Menu.objects.all().order_by('id')
        return render(request, 'edit.html', {'menu_list':menu_list, 'form':form})

def edit_menu_func(request, id):
    try:
        edit_menu = Menu.objects.get(pk = id)
    except Menu.DoesNotExist:
        raise Http404

    form = MenuForm({'menu_name':edit_menu})

    return render(request, 'edit_menu.html', {'id':id, 'edit_menu':edit_menu, 'form':form})