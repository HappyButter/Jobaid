from django.shortcuts import render 
from django.http import JsonResponse
from  job_offers.models import JobPosition
from .charts_data import languages, company_size, technologies, constracts, level
from .models import ChartsData

def statistics(request):
    context = {
        "title": "Statistics and charts",
        'app': 'statistics_and_charts',
        'page':'statistics'
    }
    return render(request, "statistics_and_charts/statistics.html", context)

def recalculate_statistics(request):
    new_data = ChartsData()
    new_data.company_size = company_size()
    new_data.experience_level = level()
    new_data.contracts = constracts()
    new_data.languages = languages()
    new_data.technologies = technologies()

    # temporary for debugging
    print('languages: ', new_data.languages)
    print('company_size: ', new_data.company_size)
    print('experience level:', new_data.experience_level)
    print('contracts:', new_data.contracts)
    print('technologies: ', new_data.technologies)

    context = {
        "title": "Statistics and charts",
        'app': 'statistics_and_charts',
        'page':'statistics'
    }
    return render(request, "statistics_and_charts/statistics.html", context)