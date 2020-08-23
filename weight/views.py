from django.shortcuts import render, redirect, Http404
from django.http.response import HttpResponse
from django.db.models import Max, Sum
from .models import Menu, Record
from .forms import RecordForm, MenuForm, SignUpForm, LoginForm
from django.views.decorators.http import require_POST
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import datetime

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
    #ホーム(/home)へのアクセスがあった場合は、こちらで処理。
    if request.path == '/home':
        return render(request, 'home.html', {'menu_list':menu_list})
    #記録確認へのアクセスがあった場合は、こちらで処理。
    elif request.path =='/result_menu':
        return render(request, 'result_menu.html', {'menu_list':menu_list})
    #url直接アクセス(/)があった場合は、こちらで処理。'/home' or '/'とすると、'/'が条件にマッチしてしまうため
    #/result_menuへのアクセスも/へのアクセスとして処理されてしまう。
    elif request.path =='/':
        return render(request, 'home.html', {'menu_list':menu_list})

@login_required
def result_list_func(request):
    #filterでmenuモデルのユーザidとログインユーザのidとを突合して、ログインユーザのレコードのみ抽出できるようにしている。
    #weight_menuはMenuモデルを指す外部キーなので、'_'をつなげてMenuモデルのuserを参照し、そのuserはUserモデルを指す外部キーなので同じように'_'をつなげてUserモデルidを参照する。
    results = Record.objects.filter(weight_menu__user__id = request.user.id).order_by('-registerd_at', 'weight_menu__id')[:100]
    return render(request, 'result_list.html', {'results':results})

@login_required
def result_edit_func(request, id):
    try:
        #メニューを保持するユーザ以外のアクセスがあった場合は後者の条件に一致せずレコードを取得できないためエラーになる。
        edit_result = Record.objects.get(id = id, weight_menu__user__id = request.user.id)
    except Menu.DoesNotExist:
        raise Http404

    if request.method == 'POST':
        form = RecordForm(request.POST)
        if form.is_valid():

            edit_result.registerd_at = request.POST['regi_date']
            edit_result.weight_record = form.cleaned_data['weight_record']
            edit_result.rep = form.cleaned_data['rep']
            edit_result.sets = form.cleaned_data['sets']
            edit_result.save()
            return redirect('result_list')
        else:
            messages.error(request, '入力欄には1以上の値を入力してください。')
            return redirect('result_edit', id)

    #RecordFormの項目に、最初に取得したmodelのデータをセットする。
    form = RecordForm({'weight_record':edit_result.weight_record, 'rep':edit_result.rep, 'sets':edit_result.sets})

    return render(request, 'result_edit.html', {'id':id, 'edit_result':edit_result, 'form':form})

@require_POST
@login_required
def result_delete_func(request, id):
    try:
        delete_record = Record.objects.get(id = id, weight_menu__user__id = request.user.id)
    except Menu.DoesNotExist:
        raise Http404
    delete_record.delete()

    return redirect('result_list')

@login_required
def input_func(request, id):
    #request.POST['regi_date']に対するバリデーションを作成すること。
    if request.method == 'POST':
        form = RecordForm(request.POST or None)
        if form.is_valid():
            register_record = Record()

            register_record.weight_record = form.cleaned_data['weight_record']
            register_record.rep = form.cleaned_data['rep']
            register_record.sets = form.cleaned_data['sets']
            
            Record.objects.create(
                weight_menu = Menu(id = id),
                weight_record = register_record.weight_record,
                rep = register_record.rep,
                sets = register_record.sets,
                #regi_dateはform.pyで定義せず、htmlに直打ちしているため、formのメソッドが適用できない。
                #従って、request.POST['フォームのid（name属性の値）']でrequestから直接取得している（https://qiita.com/nab/items/e32cde1643a010dfacb9）。
                registerd_at = request.POST['regi_date'],
            )

            #idで検索してユニークなメニューを取得するのでget
            register_menu = Menu.objects.get(id = id)
            print(register_menu)
            #messages.success(request, '記録完了')
            volume = register_record.weight_record * register_record.rep * register_record.sets
            return render(request, 'input_success.html', {'id':id, 'register_menu':register_menu, 'register_weight':register_record.weight_record, 'register_rep':register_record.rep, 'register_sets':register_record.sets, 'volume':volume})
        
        #formで定義したkg,Repともに1以上という条件を満たさない場合は、エラーメッセージを生成してinput.htmlへリダイレクトする。
        else:
            messages.error(request, '入力欄には1以上の値を入力してください。')
            return redirect('input', id)

    else:
        #メニューを保持するユーザ以外のアクセスを拒否する
        try:
            menu_user_id = Menu.objects.get(id = id)
        except Menu.DoesNotExist:
            raise Http404
        
        print('userのid', request.user.id, 'menu保持者のid', menu_user_id.user.id)
        
        if request.user.id != menu_user_id.user.id:
            print('false')
            return redirect('home')
        
        #外部キーの値を取得する時は定義した外部キーの項目名にアンダーバーを２つ続けて、取得したいデータの値を指定する。
        #DBからレコードを取得する方法を確認した記述。一応消さずに残しておくが、恐らくコメント解除しても正常動作しない。
        """ latest_rec = Record.objects.filter(weight_menu__id= id).latest('created_at')
        test_latest_created_at = Record.objects.filter(weight_menu__id= id).values().latest('created_at')
        test_latest_created_at_2 = Record.objects.filter(weight_menu__id = id).aggregate(Max('created_at'))
        print('Queryset型で取得', latest_rec)
        print('辞書型で取得', test_latest_created_at)
        print('辞書型で取得してキーを指定', test_latest_created_at['created_at'])
        print('aggregateで取得', test_latest_created_at_2)
        print('aggregateで取得してキーを指定してデータ変換', test_latest_created_at_2['created_at__max'].date())

        max_created_at = Record.objects.filter(weight_menu__id = id).aggregate(Max('created_at'))
        max_created_at_date = max_created_at['created_at__max'].date()
        print(max_created_at_date)
        weight_sum = Record.objects.filter(weight_menu__id = id, created_at__startswith = max_created_at_date).aggregate(Sum('weight_record'))
        rep_sum = Record.objects.filter(weight_menu__id = id, created_at__startswith = max_created_at_date).aggregate(Sum('rep'))
        set_sum = Record.objects.filter(weight_menu__id = id, created_at__startswith = max_created_at_date).aggregate(Sum('sets'))
        print('重量合計', weight_sum, 'Rep合計', rep_sum, 'Set合計', set_sum)
        volume = weight_sum['weight_record__sum'] * rep_sum['rep__sum']
        print(volume) """

        #home画面で選択された種目を抽出
        selected_register_menu = Menu.objects.get(id = id)
        print(selected_register_menu)
        #getの時は、空のフォームを作成してレンダリング
        form = RecordForm()
        #regi_dateの初期値をvalue属性に指定するため、今日の日付を取得し、文字列に変換してテンプレートに渡す。https://qiita.com/7110/items/4ece0ce9be0ce910ee90
        dtn = datetime.datetime.now()
        today = dtn.strftime('%Y-%m-%d')
        print(today)
    return render(request, 'input.html', {'id':id, 'selected_register_menu':selected_register_menu, 'form':form, 'today':today})

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
                
                #2020.8.12 開発当初はinput画面に前回の記録を表示していたことによる処理。表示方法を変えたので、削除した。
                """ 新規登録したメニューの記録を0kgで作成する。
                この処理がない場合、home画面で新規登録したメニューをクリックした際に、レコードを探してこれないためエラーとなる。
                new_menu_id = Menu.objects.get(user__id = request.user.id, menu_name = register_menu.menu_name)
                print(new_menu_id.id)
                Record.objects.create(
                weight_menu = Menu(id = new_menu_id.id),
                weight_record = 0.00,
                ) """

            return redirect('edit_menu')

    else:
        form = MenuForm()
        menu_list = Menu.objects.filter(user__id = request.user.id).order_by('id')
        return render(request, 'edit_menu.html', {'menu_list':menu_list, 'form':form})

@login_required
def menu_edit_func(request, id):
    try:
        edit_menu = Menu.objects.get(id = id)
    except Menu.DoesNotExist:
        raise Http404

    #メニューを保持するユーザ以外のアクセスを拒否する
    print('userのid', request.user.id, 'menu保持者のid', edit_menu.user.id)
    
    if request.user.id != edit_menu.user.id:
        print('false')
        return redirect('home')
    
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
        delete_menu = Menu.objects.get(id = id)
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
        confirm_menu = Menu.objects.get(id = id)
    except Menu.DoesNotExist:
        raise Http404
    #メニューを保持するユーザ以外のアクセスを拒否する
    print('userのid', request.user.id, 'menu保持者のid', confirm_menu.user.id) 
    if request.user.id != confirm_menu.user.id:
        return redirect('home')
    #外部キーの値を取得する時は定義した外部キーの項目名にアンダーバーを２つ続けて、取得したいデータの値を指定する。
    print(order_type)
    if order_type == 'day':
        results = Record.objects.filter(weight_menu__id = id).order_by('-created_at')
    elif order_type == 'weight':
        results = Record.objects.filter(weight_menu__id = id).order_by('-weight_record')
    
    #print(results)
    return render(request, 'result.html', {'id':id, 'confirm_menu':confirm_menu, 'results':results, 'order_type':order_type})

@login_required
def settings_func(request):
    return render(request, 'settings.html')
    