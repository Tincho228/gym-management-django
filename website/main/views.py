from django.shortcuts import render
import requests

# Create your views here.
def home(request):
    city = 'Mendoza' # Default city vaariable
    api_key = '0bd1671316868f5ad2775ab7ede5bf47' # OpenWeatherMap API key / Later to be include in .env file
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric' # API URL with city and API key
    weather_data = {} # Variable to store weather data
    error_message = None

    # Calling the OpenWeatherMap API to get weather data
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
    return render(request, 'main/dashboard.html')

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    return render(request, 'main/contact.html')

def login_view(request):
    return render(request, 'main/login.html')