from django.shortcuts import render

from django.http import HttpResponse

# Define the home view function
def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')

def checkout(request):
    return render(request, 'checkout.html')