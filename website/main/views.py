from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'main/home.html')

def dashboard(request):
    return render(request, 'main/dashboard.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

def login_view(request):
    return render(request, 'main/login.html')