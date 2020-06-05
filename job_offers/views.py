from django.shortcuts import render
from django.core.paginator import Paginator
from .forms import FilterForm, DataForm
from .models import JobOffer, JobPosition, Salary, Finances, Location
import json
from mongoengine.queryset.visitor import Q
    

def joboffers(request):
    context = {
        "title": "Job Offers",
        'app': 'job_offers',
        'page': 'offers'
    }
    offers = []

    if request.method == 'POST':
        form = FilterForm(request.POST)
        query = create_query(form)
        offers = JobPosition.objects(query)
    else:
        offers = JobPosition.objects(create_query_with_excluded_empty_technologies())

    paginator = Paginator(offers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    context['is_paginated'] = True
    context['offers_amount'] = len(offers)

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
    job_offer['offer_hash'] = json_dict['offer_hash']
    job_offer['offer_link'] = json_dict['offer_link']
    job_offer['source_page'] = json_dict['source_page']
    job_offer['date'] = json_dict['date']
    job_offer['active'] = json_dict['active']
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
        print("ADDING FILE")
        handle_uploaded_file(request.FILES['datafile'])
        print("FINISHED")
        return render(request, 'job_offers/content.html', context)

    return render(request, 'job_offers/admin.html', context)


def div_technologies(technologies):
    if technologies != None and technologies != '':
        technologies_list = [tech.strip() for tech in technologies.split(',') if tech.strip() != '']
        return technologies_list
    return None

def create_query_with_excluded_empty_technologies():
    return Q(technologies__not__size=0) | Q(languages__not__size=0)

def create_query(form):
    query = Q()
    technologies = form['technologies'].value()
    technologies_list = div_technologies(technologies)
    if technologies_list != None:
        for technology in technologies_list:
            tech_query = Q()
            tech_query = Q(languages__iexact=technology) | tech_query
            tech_query = Q(technologies__iexact=technology) | tech_query
            query = tech_query & query

    query = query & create_query_with_excluded_empty_technologies()

    experience_level = form['experience_level'].value()
    if experience_level != ['']:
        query = Q(experience_level__in=experience_level) & query

    b2b = form['b2b'].value()
    if b2b != None and b2b != False:
        query = Q(finances__contracts__b2b=True) & query

    uop = form['uop'].value()
    if uop != None and uop != False:
        query = Q(finances__contracts__uop=True) & query

    location = form['location'].value()
    if location != None and location != '':
        query = Q(location__address__iexact=location) & query

    fork_min = form['fork_min'].value()
    try:
        fork_min = int(fork_min)
        query = (Q(finances__salary__b2b__min__gte=fork_min) | Q(finances__salary__uop__min__gte=fork_min)) & query
    except:
        fork_min = None
        
    fork_max = form['fork_max'].value()
    try:
        fork_max = int(fork_max)
        query = (Q(finances__salary__b2b__max__lte=fork_max) | Q(finances__salary__uop__max__lte=fork_max)) & query
    except:
        fork_max = None

    return query
