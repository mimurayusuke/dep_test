from django import forms

class RecordForm(forms.Form):
    weight_record = forms.DecimalField(
        label='record',
        max_digits=5,
        decimal_places=2,
        required=True,
        widget=forms.NumberInput(attrs={'class': 'input_area'})
    )