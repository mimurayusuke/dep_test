from django.shortcuts import render, redirect, Http404
from django.http.response import HttpResponse
from django.db.models import Max
from .models import Menu, Record
from .forms import RecordForm, MenuForm, SignUpForm, LoginForm
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# Create your views here.

def hello_weight(request):
    return render(request, 'index.html')

@login_required
def home_func(request):
    print(request)
    print(request.path)
    print(request.user)
    print(request.user.id)
    print(request.user.is_authenticated)
    print(request.COOKIES)
    menu_list = Menu.objects.filter(user__id = request.user.id).order_by('id')
    #home.htmlとresult_menu.htmlはタイトルが異なるだけで表示画面が同じなので、
    #アクセスパスによってrenderする画面を切り替える。
    #ホームへのアクセスがあった場合は、こちらで処理。
    if request.path == '/home':
        return render(request, 'home.html', {'menu_list':menu_list})
    #記録確認へのアクセスがあった場合は、こちらで処理。
    elif request.path =='/result_menu':
        return render(request, 'result_menu.html', {'menu_list':menu_list})

@login_required
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

@login_required
def edit_menu_func(request):
    
    if request.method == 'POST':
        form = MenuForm(request.POST or None)
        if form.is_valid():
            register_menu = Menu()
            print(form)
            register_menu.menu_name = form.cleaned_data['menu_name']
            register_menu.user = request.user

            #登録するメニューが既に存在する場合はエラーメッセージを返し、存在しない時に登録する。
            if  Menu.objects.filter(user__id = request.user.id, menu_name = register_menu.menu_name).exists():
                error_message = "は既に登録されています。"
                form = MenuForm()
                menu_list = Menu.objects.filter(user__id = request.user.id).order_by('id')
                return render(request, 'edit_menu.html', {'menu_list':menu_list, 'form':form, 'error_message':error_message, 'registered_menu':register_menu.menu_name})
            else:
                Menu.objects.create(
                    menu_name = register_menu.menu_name,
                    user = register_menu.user
                )
                #新規登録したメニューの記録を0kgで作成する。
                #この処理がない場合、home画面で新規登録したメニューをクリックした際に、レコードを探してこれない
                #ためエラーとなる。
                new_menu_id = Menu.objects.get(user__id = request.user.id, menu_name = register_menu.menu_name)
                print(new_menu_id.id)
                Record.objects.create(
                weight_menu = Menu(id = new_menu_id.id),
                weight_record = 0.00,
            )

            return redirect('edit_menu')

    else:
        form = MenuForm()
        menu_list = Menu.objects.filter(user__id = request.user.id).order_by('id')
        return render(request, 'edit_menu.html', {'menu_list':menu_list, 'form':form})

@login_required
def edit_func(request, id):
    try:
        edit_menu = Menu.objects.get(pk = id)
    except Menu.DoesNotExist:
        raise Http404
    
    if request.method == 'POST':
        form = MenuForm(request.POST)
        if form.is_valid():
            #入力された種目名が既存種目名と同じ場合は、エラーメッセージを表示する。
            print('not')
            if  Menu.objects.filter(menu_name = form.cleaned_data['menu_name'], user__id = request.user.id).exists():
                error_message = "は既に使用されています。"
                return render(request, 'edit.html', {'id':id, 'input_menu':form.cleaned_data['menu_name'], 'form':form, 'error_message':error_message})

            edit_menu.menu_name = form.cleaned_data['menu_name']
            edit_menu.save()
            return redirect('edit_menu')

    #MenuFormの項目であるmenu_nameに対して、↑で取得したmodelのデータをセットする。
    form = MenuForm({'menu_name':edit_menu.menu_name})

    return render(request, 'edit.html', {'id':id, 'edit_menu':edit_menu, 'form':form})

@require_POST
@login_required
def delete_func(request, id):
    try:
        delete_menu = Menu.objects.get(pk = id)
    except Menu.DoesNotExist:
        raise Http404
    delete_menu.delete()

    return redirect('edit_menu')

def signup_func(request):
    if request.method == 'POST':
        print(request.POST)
        form = SignUpForm(request.POST)
        #formの中身を確認することで、エラーになっている内容が分かる。
        print(form)
        if form.is_valid():
            user = form.save()
            print(user.id)#user.idで登録されているユーザのpkを参照できる。
            login(request, user)
            #検証段階のため、testにredirectしている。
            #return redirect('test', pk=user.pk)
            return redirect('home')
        else:
            return render(request, 'signup.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

def login_func(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print('ユーザ名' + username + ' パスワード' + password)
        print(request.POST)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            print(str(user) + 'login ok')
            login(request, user)
            #これでhome/user.pk/でアクセスできる。
            #return redirect('home', pk=user.pk)
            #検証段階のため、testにredirectしている。
            return redirect('home')
        else:
            print('no valid')
            error_message = "ユーザ名またはパスワードが不正です。"
            form = LoginForm()
            return render(request, 'login.html', {'form': form, 'error_message': error_message})    
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

@login_required
def logout_func(request):
    logout(request)
    return redirect('login')

@login_required
def account_func(request):
    return render(request, 'account.html')

@login_required
def result_func(request, id, order_type):
    try:
        confirm_menu = Menu.objects.get(pk = id)
    except Menu.DoesNotExist:
        raise Http404
    #外部キーの値を取得する時は定義した外部キーの項目名にアンダーバーを２つ続けて、取得したいデータの値を指定する。
    print(order_type)
    if order_type == 'day':
        results = Record.objects.filter(weight_menu__id = id).order_by('-created_at')
    elif order_type == 'weight':
        results = Record.objects.filter(weight_menu__id = id).order_by('-weight_record')
    
    print(results)
    return render(request, 'result.html', {'id':id, 'confirm_menu':confirm_menu, 'results':results, 'order_type':order_type})