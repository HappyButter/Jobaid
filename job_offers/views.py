from django.shortcuts import render
from django.http import HttpResponse # just temporary until templates will be created

def home(request):
    return HttpResponse('<h1>job offers page</h1>')
