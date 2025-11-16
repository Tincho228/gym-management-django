from django.shortcuts import render

# Create your views here.
def home(request):
    #return render(request, 'main/home.html')
    return HttpResponse("Gym Management App is Live!")