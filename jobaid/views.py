from django.shortcuts import render
from .utils import make_object_from_form 
from .forms import AddPositionForm

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
        new_job_position = make_object_from_form(form)
        new_job_position.save()
    else:
        form = AddPositionForm()
        context['form'] = form

    return render(request, 'jobaid/contribute.html', context)