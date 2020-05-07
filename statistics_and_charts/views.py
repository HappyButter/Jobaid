from django.shortcuts import render


def statistics(request):
    context = {
        "title": "Statistics and charts",
    }

    return render(request, "statistics_and_charts/statistics_and_charts.html", context)