import datetime
import requests
from django.shortcuts import render
from django.http import HttpResponse
from .API_KEY import API_KEY



def main(request):
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
    responce = requests.get(weather_url.format(city, api_key)).json()
    lat = responce['coord']['lat']
    lon = responce['coord']['lon']
    forecast_responce = requests.get(forecast_url.format(lat, lon, api_key)).json()
    temperature_in_celsius = round(responce['main']['temp'] - 273.15, 2)
    weather_description = responce['weather'][0]['description']
    weather_icon = responce['weather'][0]['icon']

    weather_info = {
        'city': city,
        'temperature': temperature_in_celsius,
        'description': weather_description,
        'icon': weather_icon
    }

    forecasts_list = []

    for forecast in forecast_responce['daily'][:5]:
        forecasts_list.append({
            'day': datetime.datetime.fromtimestamp(forecast['dt']).strftime('%A'),
            'min_temp': round(forecast['temp']['min'] - 273.15, 2),
            'max_temp': round(forecast['temp']['max'] - 273.15, 2),
            'description': forecast['weather'][0]['description'],
            'icon': forecast['weather'][0]['icon']
        })

    return weather_info, forecasts_list