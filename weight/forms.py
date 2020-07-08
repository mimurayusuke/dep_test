from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Menu

class RecordForm(forms.Form):
    weight_record = forms.DecimalField(
        label='record',
        max_digits=5,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'input_area'})
    )

class MenuForm(forms.Form):
    menu_name = forms.CharField(
        label='menu',
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'input_area'})
    )

#class MultiSelectForm(forms.Form):
#    menu_name = forms.MultipleChoiceField(
#        label_suffix='menu',
#        widget=forms.SelectMultiple(attrs={'class': 'select_menu'})
#    )

class SignUpForm(UserCreationForm):
    username = forms.CharField(
        widget = forms.TextInput(attrs={'id': 'sign_up_name', 'class': 'input_area', 'name': 'username'})
        )
    password1 = forms.CharField(
        widget = forms.PasswordInput(attrs={'id': 'sign_up_pass1', 'class': 'input_area', 'name': 'password1'})
        )
    password2 = forms.CharField(
        widget = forms.PasswordInput(attrs={'id': 'sign_up_pass2', 'class': 'input_area', 'name': 'password2'})
        )

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget = forms.TextInput(attrs={'id': 'login_name', 'class': 'input_area', 'name': 'username'})
        )
    password = forms.CharField(
        widget = forms.PasswordInput(attrs={'id': 'login_pass', 'class': 'input_area', 'name': 'password'})
        )