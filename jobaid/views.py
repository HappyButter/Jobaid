from django.shortcuts import render

from .utils import make_object_from_form 
from .forms import AddPositionForm
from .utils import EmptyInput, NotEnoughData

def about(request):
    context = {
        'title': 'About',
        'app': 'jobaid',
        'page':'about'
    }
    return render(request, 'jobaid/about.html', context)

def contribute(request):
    context = {
        "title": "Job Offers",
        'app': 'jobaid',
        'page': 'contribute'
    }
    offers = []

    if request.method == 'POST':
        form = AddPositionForm(request.POST)
        try:
            new_job_position = make_object_from_form(form)
            new_job_position.save()
            context['is_input_valid'] = True
        except EmptyInput:
            context['is_input_valid'] = False
            context['invalid_input_message'] = 'There are empty fields'
        except NotEnoughData:
            context['is_input_valid'] = False
            context['invalid_input_message'] = 'Number of technologies is less than 4'

    else:
        form = AddPositionForm()
        context['form'] = form

    return render(request, 'jobaid/contribute.html', context)