from django.http.response import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request = request, context = {}, template_name = 'dashboard/index.html')


def service(request):
    return render(request = request, context = {}, template_name = 'dashboard/service.html')