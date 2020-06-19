from django import forms
from common.utils import EXPERIENCE_CHOICES, CONTRACT_NAME

class AddPositionForm(forms.Form):
    location = forms.CharField(max_length=100)
    company_size = forms.IntegerField()
    experience_level = forms.MultipleChoiceField(choices=EXPERIENCE_CHOICES)
    technologies = forms.CharField(max_length=100)
    contract = forms.ChoiceField(choices=CONTRACT_NAME, widget=forms.RadioSelect)
    fork_min = forms.IntegerField()
    fork_max = forms.IntegerField()
