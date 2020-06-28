from django import forms

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
        widget=forms.TextInput(attrs={'class': 'input_menu'})
    )