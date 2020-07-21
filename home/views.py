from django.shortcuts import render

# Create your views here.


def index(request):
    """ view to return index.html"""
    return render(request, 'home/index.html')
