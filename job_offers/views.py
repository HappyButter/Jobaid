from django.shortcuts import render
from django.core.paginator import Paginator

from .models import JobOffer
from .utils import extract_filters_from_url, create_query, create_query_with_excluded_empty_technologies

def joboffers(request):
    context = {
        "title": "Job Offers",
        'app': 'job_offers',
        'page': 'offers'
    }
    offers = []

    # if len(request.GET):
    offers = JobOffer.objects(create_query(request.GET))
    # else:
    #     offers = JobOffer.objects(create_query_with_excluded_empty_technologies())
        
    filters = extract_filters_from_url(request)
    paginator = Paginator(offers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context['filters'] = filters
    context['inputs'] = request.GET
    context['page_obj'] = page_obj
    context['is_paginated'] = True
    context['offers_amount'] = len(offers)

    return render(request, 'job_offers/content.html', context)

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