from django.shortcuts import render


def joboffers(request):
    context = {
        "title": "Job Offers",
    }
    return render(request, "job_offers/job_offers.html", context)
