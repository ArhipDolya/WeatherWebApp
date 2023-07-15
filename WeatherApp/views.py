import datetime
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from .API_KEY import API_KEY
from .forms import RegisterUserForm
from django.contrib.auth.forms import AuthenticationForm 
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext as _


def local_test(request):
    return render(request, 'local.html', {'hello': _('Hello')})


def homepage(request):
    return render(request, 'homepage.html')

@login_required
def weather_view(request):
    api_key = API_KEY
    weather_url = 'https://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    forecast_url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exlude=current,minutely,hourly,alerts&appid={}'

    if request.method == 'POST':
        city1 = request.POST['city1']
        city2 = request.POST.get('city2', None)

        weather_info1, forecasts_info1 = get_weather_forecast(city1, API_KEY, weather_url, forecast_url)

        if city2:
            weather_info2, forecasts_info2 = get_weather_forecast(city2, API_KEY, weather_url, forecast_url)
        else:
            weather_info2, forecasts_info2 = None, None

        content = {
            'weather_info1': weather_info1,
            'forecasts_info1': forecasts_info1,
            'weather_info2': weather_info2,
            'forecasts_info2': forecasts_info2,
        }

        return render(request, 'index.html', content)

    else:
        return render(request, 'index.html')
    

def get_weather_forecast(city, api_key, weather_url, forecast_url):
    response = requests.get(weather_url.format(city, api_key)).json()

    if 'coord' not in response:
        # Handles the error when 'coord' key is not found in the response
        return None, None

    lat = response['coord']['lat']
    lon = response['coord']['lon']
    forecast_response = requests.get(forecast_url.format(lat, lon, api_key)).json()
    temperature_in_celsius = round(response['main']['temp'] - 273.15, 2)
    weather_description = response['weather'][0]['description']
    weather_icon = response['weather'][0]['icon']

    weather_info = {
        'city': city,
        'temperature': temperature_in_celsius,
        'description': weather_description,
        'icon': weather_icon
    }

    forecasts_list = []

    for forecast in forecast_response['daily'][:5]:
        forecasts_list.append({
            'day': datetime.datetime.fromtimestamp(forecast['dt']).strftime('%A'),
            'min_temp': round(forecast['temp']['min'] - 273.15, 2),
            'max_temp': round(forecast['temp']['max'] - 273.15, 2),
            'description': forecast['weather'][0]['description'],
            'icon': forecast['weather'][0]['icon']
        })

    return weather_info, forecasts_list


def user_registration_view(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        
        if form.is_valid():
            user = form.save()
            user.password = make_password(form.cleaned_data['password1'])
            user.save()
            messages.success(request, 'Successful registration!')
            return redirect('/')
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = RegisterUserForm()

    return render(request, 'registration/registration.html', {'form': form})
    

def user_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('weather')
            else:
                messages.error(request, "Invalid user !")
        
    else:
        form = AuthenticationForm()

    return render(request, 'registration/login.html', {'form': form})


def logout_user_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully")
    return redirect('/')