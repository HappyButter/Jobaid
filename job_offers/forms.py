from django import forms

EXPERIENCE_CHOICES = (
    ('Junior', 'Junior'),
    ('Mid', 'Mid'),
    ('Senior', 'Senior'),
)

class FilterForm(forms.Form):
    technologies = forms.CharField(max_length=100)
    experience_level = forms.MultipleChoiceField(choices=EXPERIENCE_CHOICES) 
    b2b = forms.BooleanField()
    uop = forms.BooleanField()
    location = forms.CharField(max_length=100)
    fork_min = forms.IntegerField()
    fork_max = forms.IntegerField()

class DataForm(forms.Form):
    datafile = forms.FileField()
    password = forms.CharField()

CONTRACT_NAME = {
    ('b2b', 'b2b'),
    ('uop','uop'),
}

class AddPositionForm(forms.Form):
    location = forms.CharField(max_length=100)
    company_size = forms.IntegerField()
    experience_level = forms.MultipleChoiceField(choices=EXPERIENCE_CHOICES)
    technologies = forms.CharField(max_length=100)
    contract = forms.ChoiceField(choices=CONTRACT_NAME, widget=forms.RadioSelect)
    salary_from = forms.IntegerField()
    salary_to = forms.IntegerField()
