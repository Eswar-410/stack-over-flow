from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, 'home.html')


def navbar(request):
    return render(request, 'partials/navbar.html')
