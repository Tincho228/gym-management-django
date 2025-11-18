from django.shortcuts import render
import requests
from datetime import datetime
from django.conf import settings # Import settings to access environment variables

# Create your views here.
def home(request):
    city = 'Mendoza' # Default city vaariable
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

    # Returning the rendered template with weather data and error message
    return render(request, 'main/home.html', {'weather_data': weather_data, 'error_message': error_message})

def dashboard(request):
    city = 'Mendoza' # Default city vaariable
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
        'city': city_name,
        # Pass the list of the 5 daily forecasts to the template
        'daily_forecasts': list(daily_forecasts.values()), 
    }

    # Returning the rendered template with weather data and error message

    return render(request, 'main/dashboard.html', {'error_message': error_message, 'context': context})

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

def login_view(request):
    return render(request, 'main/login.html')