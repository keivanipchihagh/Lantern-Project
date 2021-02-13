from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse(request.META['HTTP_HOST'])