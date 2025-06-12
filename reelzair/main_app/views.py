from django.shortcuts import render

from django.http import HttpResponse

# Define the home view function
def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request, 'about.html')

def checkout(request):
    return render(request, 'checkout.html')

def cart(request):
    return render(request, 'cart.html')

def product(request):
    return render(request, 'product.html')

def confirmation(request):
    return render(request, 'confirmation.html')

def figma(request):
    # Default Figma project URL - replace with your actual Figma project URL
    figma_url = request.GET.get('url', 'https://www.figma.com/file/YourDefaultFigmaFileID/YourDefaultFigmaFileName')
    return render(request, 'figma.html', {'figma_url': figma_url})
