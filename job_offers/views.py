from django.shortcuts import render
from .forms import FilterForm
from .models import JobOffer, JobPosition

def pluj(f_technologies):
    if f_technologies != None:
        f_technologies_list = f_technologies.replace(' ','').split(",")
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
        f_technologies_list = pluj(f_technologies)

        f_experience_level = form['experience_level'].value()
        if f_experience_level != None:
            f_experience_level = f_experience_level[0]

        f_b2b = form['b2b'].value()

        f_uop = form['uop'].value()

        f_location = form['location'].value()

        f_fork_min = form['fork_min'].value()
        f_fork_max = form['fork_max'].value()

        offers = JobPosition.objects(technologies=f_technologies,
                                    experience_level=f_experience_level,
                                    finances__contracts__b2b=f_b2b,
                                    # finances__contracts__uop=f_uop,
                                    location__address=f_location,
                                    finances__salary__b2b__min__gte=int(f_fork_min),
                                    finances__salary__b2b__max__lte=int(f_fork_max),
                                    )
        print(offers)
        # self.context['offers'] = offers
    else:
        form = FilterForm()
        context['form'] = form
    return render(request, 'job_offers/content.html', context)