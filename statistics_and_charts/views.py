from django.shortcuts import render 
from django.http import JsonResponse
from  job_offers.models import JobPosition


def statistics(request):
    context = {
        "title": "Statistics and charts",
        'app': 'statistics_and_charts',
        'page':'statistics'
    }
    return render(request, "statistics_and_charts/statistics.html", context)


def example(request): 
    offers = JobPosition.objects()
    stats = {
        'JavaScript': 0,
        'Python': 0,
        'Java': 0,
        'C#': 0,
        'PHP': 0,
        'C++': 0
    }
    
    for offer in offers:
        lowercase_languages = [lang.lower() for lang in offer['languages']]
        if 'javascript' in lowercase_languages:
            stats['JavaScript'] += 1
        if 'python' in lowercase_languages:
            stats['Python'] += 1
        if 'java' in lowercase_languages:
            stats['Java'] += 1
        if 'c#' in lowercase_languages:
            stats['C#'] += 1
        if 'php' in lowercase_languages:
            stats['PHP'] += 1
        if 'c++' in lowercase_languages:
            stats['C++'] += 1     

    return JsonResponse(stats)
        
