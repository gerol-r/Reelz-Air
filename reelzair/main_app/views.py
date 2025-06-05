from django.shortcuts import render

from django.http import HttpResponse

# Define the home view function
def home(request):
    # Send a simple HTML response
    return HttpResponse('<h1>Welcome to Reelz Air</h1>')
def about(request):
    return render(request, 'about.html')
