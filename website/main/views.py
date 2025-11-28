from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from datetime import datetime
from website import settings
from .forms import CustomUserCreationForm, NewMembershipForm
from .models import Instructor, Membership, Routine, Exercise, UserProfile


def home(request):
    # user information and routines
    user = request.user
    role = None
    routines = None

    if user.is_authenticated:
        role = "admin" if hasattr(user, "profile") and user.profile.is_admin else "client"

    # weather data
    city = 'Mendoza' # Default city variable
    api_key = settings.OPENWEATHER_API_KEY # OpenWeatherMap API key / Later to be include in .env file
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric' # API URL with city and API key
    weather_data = {} # Variable to store weather data
    error_message = None

    # Calling the OpenWeatherMap API to get current weather data
    try:    
        response = requests.get(url).json()
        if response.get('cod') != 200:
            error_message = response.get('message', 'Error retrieving weather data.')

        weather_data = {
            'city': response['name'],
            'temperature': response['main']['temp'],
            'description': response['weather'][0]['description'],
            'wind_speed': response['wind']['speed'],
            'icon': response['weather'][0]['icon'],
        }
    except ValueError as e:
        error_message = str(e)
        
    context = {
        "user": user,
        "role": role,
        "routines": routines,
        "weather_data": weather_data,
        "error_message": error_message,
    }

    # Returning the rendered template with weather data and error message
    return render(request, 'main/home.html', context)

# Dashboard is only visible to logged users
@login_required
def dashboard(request):
    user = request.user
    role = "admin" if user.profile.is_admin else "client"
    routines = None
    if role == "admin" and hasattr(user, "instructor_profile"):
        routines = user.instructor_profile.routines.all()
    
    # Memberhsips info
    membership_types = Membership.PLAN_CHOICES

    # All members
    all_memberships = Membership.objects.select_related("user").all()

    # Weather
    city = 'Mendoza' # Default city variable
    api_key = settings.OPENWEATHER_API_KEY # OpenWeatherMap API key / Later to be include in .env file
    url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric' # API URL with city and API key
    weather_data = {} # Variable to store weather data
    error_message = None

    # Calling the OpenWeatherMap API to get 5 days forecast weather data

    try:    
        response = requests.get(url).json()
        if response.get('cod') != 200:
            error_message = response.get('message', 'Error retrieving weather data.')

        city_name = response['city']['name']
        forecast_list = response['list']

        
    except ValueError as e:
        error_message = str(e)

    # Dictionary to store one forecast entry per day
    daily_forecasts = {}

    for entry in forecast_list:
        # Convert the 'dt_txt' string (e.g., "2025-11-18 12:00:00") to a datetime object
        dt_object = datetime.strptime(entry['dt_txt'], '%Y-%m-%d %H:%M:%S')
        date_key = dt_object.date() # Get the date part only (YYYY-MM-DD)
        # We want to show a single entry for each of the next 5 days. 
        # A common practice is to use the mid-day (e.g., 12:00:00) forecast.
        # Since the API data is 3-hourly, we'll grab the first entry for each day.
        # Once a day is recorded, skip subsequent entries for that day.
        if date_key not in daily_forecasts and len(daily_forecasts) < 5:
            # Store the data for the template
            daily_forecasts[date_key] = {
                'temp': entry['main']['temp'],
                'description': entry['weather'][0]['description'].capitalize(),
                'wind_speed': entry['wind']['speed'],
                'icon_code': entry['weather'][0]['icon'],
                'time_str': dt_object.strftime('%H:%M'), # Format as Hours:Minutes
                'day_name': dt_object.strftime('%A'), # Get the full day name
            }

    context = {
        "role": role,
        "routines": routines,
        "membership_types": membership_types,
        "all_memberships": all_memberships,
        'city': city_name,
        # Pass the list of the 5 daily forecasts to the template
        'daily_forecasts': list(daily_forecasts.values()), 
        'error_message': error_message,
    }

    # Returning the rendered template with weather data and error message

    return render(request, 'main/dashboard.html', context)

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

def login_view(request):
    # return render(request, 'main/login.html')
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)  # built-in
        if form.is_valid():
            user = form.get_user()
            login(request, user)         # sets session
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard')  # or use next param
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request, "main/login.html", {"form": form})

def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('add-membership')
        else:
            messages.error(request, "Please fix the errors below.")
    else:
        form = CustomUserCreationForm()

    return render(request, "main/register.html", {"form": form})

def add_membership_view(request):
    if request.user.is_authenticated:
        if hasattr(request.user, "membership"):
            return redirect("dashboard")
        if request.method == "POST":
            form = NewMembershipForm(request.POST)
            if form.is_valid():
                plan = form.cleaned_data["plan_type"]
                duration = form.cleaned_data["duration_days"]
                Membership.objects.create(
                    user = request.user,
                    plan_type = plan,
                    duration_days = duration
                )
                return redirect('dashboard')
        else:
            form = NewMembershipForm()
    return render(request, 'main/add-membership.html', {"form": form})

def logout_view(request):
    logout(request)
    return redirect('home')
