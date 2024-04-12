import os
import requests
import json
from string import Template
import datetime

APP_CONFIG  =  {
    'API_KEY' : os.environ.get('API_KEY'),
    'URL_WEATHER_CURRENT' : os.environ.get('URL_WEATHER_CURRENT'),
    'URL_WEATHER_5_DAYS' : os.environ.get('URL_WEATHER_5_DAYS'),
    'URL_GEOCODE_LOCATION': os.environ.get('URL_GEOCODE_LOCATION'),
}

def get_geocode_location_info(lat : str, lon: str):
    template = Template(APP_CONFIG['URL_GEOCODE_LOCATION'])
    url = template.substitute(
        lat=lat,
        lon=lon,
        appid=APP_CONFIG['API_KEY'])
    
    response = requests.get(url=url)
    if response.status_code != 200:
        raise Exception("API error")
    
    return json.loads(response.text)

def get_current_forecast(lat : str, lon: str):
    template = Template(APP_CONFIG['URL_WEATHER_CURRENT'])
    url = template.substitute(
        lat=lat,
        lon=lon,
        appid=APP_CONFIG['API_KEY'])
    
    response = requests.get(url=url)
    if response.status_code != 200:
        raise Exception("API error")
    
    return json.loads(response.text)

def get_5_days_forecast(lat : str, lon: str, cnt: int):
    template = Template(APP_CONFIG['URL_WEATHER_5_DAYS'])
    url = template.substitute(
        lat=lat,
        lon=lon,
        appid=APP_CONFIG['API_KEY'],
        cnt=cnt)
    
    response = requests.get(url=url)
    if response.status_code != 200:
        raise Exception("API error")
    
    return json.loads(response.text)

def exact_weather_data(data):
    temperatures = []
    daily_dates = []
    pressure = []
    humidity = []

    for item in data['list']:
        temperatures.append(item['main']['temp_max'])
        pressure.append(item['main']['pressure'])
        humidity.append(item['main']['humidity'])
        daily_dates.append(item['dt_txt'])

    return temperatures, daily_dates, pressure, humidity