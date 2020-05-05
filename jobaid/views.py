from django.shortcuts import render


def home(request):
    context = {
        "title": "Home",
    }
    return render(request, "jobaid/home.html", context)


def about(request):
    context = {
        "title": "About",
    }
    return render(request, "jobaid/about.html", context)


