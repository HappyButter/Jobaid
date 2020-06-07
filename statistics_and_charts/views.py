
from django.shortcuts import render 
from django.http import JsonResponse

from .models import ChartsData
from .utils import recalculate_statistics

def statistics(request):
    context = {
        "title": "Statistics and charts",
        'app': 'statistics_and_charts',
        'page':'statistics'
    }
    return  render(request, 'statistics_and_charts/statistics.html', context)


def get_statistics_data(request):
    recalculate_statistics() # baaaardzo tymczasowo, docelowo ta funkcja będzie wywoływana w momencie wrzucania przez nas nowych plików
    latest_statictscs = ChartsData.objects()[0]
    # latest_statictscs = [elem.to_json() for elem in latest_statictscs]  --- cos w tym stylu
    latest_statictscs = {
        'languages': latest_statictscs.languages,
        'technologies': latest_statictscs.technologies,
        'experience_level': latest_statictscs.experience_level,
        'contracts': latest_statictscs.contracts,
        'company_size': latest_statictscs.company_size,
    } # to tak dla testów na chwile
    return JsonResponse(latest_statictscs, safe=False)