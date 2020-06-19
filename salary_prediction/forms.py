from django import forms

EXPERIENCE_CHOICES =(
    ("Junior", "Junior"),
    ("Mid", "Mid"),
    ("Senior", "Senior"),
)

class PredictionForm(forms.Form):
    technologies = forms.CharField(max_length=100)
    experience_level = forms.MultipleChoiceField(choices=EXPERIENCE_CHOICES) 
    location = forms.CharField(max_length=100)
    b2b = forms.BooleanField()
    uop = forms.BooleanField()