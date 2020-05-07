from django.shortcuts import render


# def home(request):
#     context = {
#         'title': 'Home',
#         'app': 'jobaid',
#         'page':'home'
#     }
#     return render(request, 'jobaid/home.html', context)


def about(request):
    context = {
        'title': 'About',
        'app': 'jobaid',
        'page':'about'
    }
    return render(request, 'jobaid/about.html', context)


