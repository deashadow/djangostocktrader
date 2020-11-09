from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse

# Create your views here.



def home( request):
    return render( request, 'home.html')

def about( request):
    return render( request, 'about.html')

def contact( request):
    return render( request, 'contact.html')