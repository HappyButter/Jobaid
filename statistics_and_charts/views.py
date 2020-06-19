from django.shortcuts import render 
from django.http import JsonResponse

from .models import BarChartsData, PieChartsData
from .utils import recalculate_statistics

def statistics(request):
    context = {
        'title': 'Statistics and charts',
        'app': 'statistics_and_charts',
        'page':'statistics'
    }
    return  render(request, 'statistics_and_charts/statistics.html', context)


def get_statistics_data(request):
    # recalculate_statistics()
    return JsonResponse({}, safe=False)


def get_pie_charts_data(request):
    latest_statictscs = PieChartsData.objects()[0]
    latest_statictscs = {
        'languages': latest_statictscs.languages,
        'experience_level': latest_statictscs.experience_level,
        'contracts': latest_statictscs.contracts
    }
    return JsonResponse(latest_statictscs, safe=False)


def get_bar_charts_data(request):
    latest_statictscs = BarChartsData.objects()[0]
    latest_statictscs = {
        'technologies': latest_statictscs.technologies,
        'company_size': latest_statictscs.company_size
    }
    return JsonResponse(latest_statictscs, safe=False)