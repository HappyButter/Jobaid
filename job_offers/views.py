from django.shortcuts import render
from .forms import FilterForm, DataForm
from .models import JobOffer, JobPosition, Salary, Finances, Location
import json
from mongoengine.queryset.visitor import Q

def div_technologies(f_technologies):
    if f_technologies != None and f_technologies != '':
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

        query = Q()

        f_technologies = form['technologies'].value()
        f_technologies_list = div_technologies(f_technologies)
        if f_technologies_list != None:
            query = Q(technologies__in=f_technologies_list) & query

        # f_experience_level = form['experience_level'].value()
        # if f_experience_level != None:
        #     query = Q(experience_level__in=f_experience_level) | query

        f_b2b = form['b2b'].value()
        if f_b2b != None and f_b2b != False:
            query = Q(finances__contracts__b2b=f_b2b) & query

        f_uop = form['uop'].value()
        if f_uop != None and f_uop != False:
            query = Q(finances__contracts__uop=f_uop) & query

        f_location = form['location'].value()
        if f_location != None and f_location != '':
            query = Q(location__address__iexact=f_location) & query

        f_fork_min = form['fork_min'].value()
        try:
            f_fork_min = int(f_fork_min)
            query = Q(finances__salary__b2b__min__gte=f_fork_min) & query
        except:
            f_fork_min = None
            

        f_fork_max = form['fork_max'].value()
        try:
            f_fork_max = int(f_fork_max)
            query = Q(finances__salary__b2b__max__lte=f_fork_max) & query
        except:
            f_fork_max = None


        print(query)

        offers = JobPosition.objects(query)[:20]
        
        print(f'znalezione oferty: {offers}')
        context['offers'] = offers
    else:
        form = FilterForm()
        context['form'] = form
    return render(request, 'job_offers/content.html', context)



def json_dict_to_model(json_dict):
    job_offer = JobOffer()
    salary = Salary()
    location = Location()
    finances = Finances()
    job_offer['title'] = json_dict['title']
    location['address'] = json_dict['location']['address']
    #location['coordinates'] = json_dict['location']['coordinates']    #for future
    job_offer['location'] = location
    job_offer['company'] = json_dict['company']
    job_offer['company_size'] = json_dict['company_size']
    job_offer['experience_level'] = json_dict['experience_level']
    job_offer['languages'] = json_dict['languages']
    job_offer['technologies'] = json_dict['technologies']
    salary['b2b'] = json_dict['finances']['salary']['b2b']
    salary['uop'] = json_dict['finances']['salary']['uop']
    finances['salary'] = salary
    finances['contracts'] = json_dict['finances']['contracts']
    job_offer['finances'] = finances
    job_offer['hash'] = json_dict['hash']
    job_offer['offer_link'] = json_dict['offer_link']
    job_offer['source_page'] = json_dict['source_page']
    job_offer.save()

def handle_uploaded_file(json_file):
    json_data = json_file.read()
    json_dict_list = json.loads(json_data)
    for json_dict in json_dict_list:
        json_dict_to_model(json_dict)


def admin(request):
    context = {
        "title": "Job Offers",
        'app': 'job_offers',
        'page': 'offers'
    }
    if request.method == 'POST':
        print("POST FILE REQUEST")
        data_json = DataForm(request.POST, request.FILES)
        if data_json.is_valid():
            print("VALID FORM")
            handle_uploaded_file(request.FILES['datafile'])
            print("FINISHED")
        return render(request, 'job_offers/content.html', context)

    return render(request, 'job_offers/admin.html', context)
