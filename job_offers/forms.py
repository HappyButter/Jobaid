from django import forms

class DataForm(forms.Form):
    title = forms.CharField()
    file = forms.FileField()