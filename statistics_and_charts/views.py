from django.shortcuts import render


def statistics(request):
    context = {
        "title": "Statistics and charts",
        'app': 'statistics_and_charts',
        'page':'statistics'
    }

    return render(request, "statistics_and_charts/statistics.html", context)