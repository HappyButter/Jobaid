from django.shortcuts import render


def joboffers(request):
    context = {
        "title": "Job Offers",
        'app': 'job_offers',
        'page': 'offers'
    }
    return render(request, "job_offers/content.html", context)
