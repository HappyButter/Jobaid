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
    recalculate_statistics()
    latest = ChartsData.objects()
    return JsonResponse(latest)