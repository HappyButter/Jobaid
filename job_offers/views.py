from django.shortcuts import render
from .forms import FilterForm
from .models import JobOffer, JobPosition

def div_technologies(f_technologies):
    if f_technologies != None:
        f_technologies_list = f_technologies.split(",")
        for tech in f_technologies_list:
            tech.strip()
        return f_technologies_list
    return None

def joboffers(request):
    context = {
        "title": "Job Offers",
        'app': 'job_offers',
        'page': 'offers'
    }

    if request.method == 'POST':
        form = FilterForm(request.POST)

        f_technologies = form['technologies'].value()
        f_technologies_list = div_technologies(f_technologies)

        f_experience_level = form['experience_level'].value()

        f_b2b = form['b2b'].value()

        f_uop = form['uop'].value()

        f_location = form['location'].value()

        f_fork_min = form['fork_min'].value()
        f_fork_max = form['fork_max'].value()

        offers = JobPosition.objects(
            technologies=f_technologies,
            experience_level__in=f_experience_level,
            finances__contracts__b2b=f_b2b,
            finances__contracts__uop=f_uop,
            location__address=f_location,
            finances__salary__b2b__min__gte=int(f_fork_min),
            finances__salary__b2b__max__lte=int(f_fork_max),
        )
        
        context['offers'] = offers
    else:
        form = FilterForm()
        context['form'] = form
    return render(request, 'job_offers/content.html', context)