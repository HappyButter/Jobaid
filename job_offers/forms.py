from django import forms

EXPERIENCE_CHOICES =(
    ("Junior", "Junior"),
    ("Mid", "Mid"),
    ("Senior", "Senior"),
)

class FilterForm(forms.Form):
    technologies = forms.CharField(max_length=100)
    experience_level = forms.MultipleChoiceField(choices=EXPERIENCE_CHOICES) 
    b2b = forms.BooleanField()
    uop = forms.BooleanField()
    address = forms.CharField(max_length=100)
    fork_min = forms.IntegerField()
    fork_max = forms.IntegerField()

class DataForm(forms.Form):
    datafile = forms.FileField()
    password = forms.CharField()