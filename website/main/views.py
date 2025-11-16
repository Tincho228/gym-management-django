#from django.shortcuts import render
#
## Create your views here.
#def home(request):
#    return render(request, 'main/home.html')

from django.http import HttpResponse

def home(request):
    return HttpResponse("Gym Management App is Live!")