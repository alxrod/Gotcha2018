from django import forms

class LocForm(forms.Form):
    position = forms.CharField(label='position', max_length=100)