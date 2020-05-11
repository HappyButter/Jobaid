from django import forms

class FilterForm(forms.Form):
    technologies = forms.CharField()
    b2b = forms.BooleanField()
    uop = forms.BooleanField()
    location = forms.CharField()
    forks = forms.BooleanField()
