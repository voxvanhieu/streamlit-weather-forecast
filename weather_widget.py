import streamlit.components.v1 as components
from jinja2 import Template
from datetime import datetime, timedelta

def add_second_to_unix_time(unix_utc_time : int, seconds : int):
    # Convert the Unix UTC time to a datetime object
    utc_time = datetime.fromtimestamp(unix_utc_time)

    # Add a second to the datetime object
    utc_time = utc_time + timedelta(seconds=seconds)
    
    return utc_time.strftime('%H:%M')

def draw_weather_forecast(forecast_data: dict):
    
    location = forecast_data['location'][0]
    current = forecast_data['current']
    future = forecast_data['future']
    
    city = location['name']
    if 'vi' in location['local_names']:
        city = location['local_names']['vi']
        
    description = current['weather'][0]['description']
    icon = current['weather'][0]['icon']
    
    timezonesec = int(current['timezone'])
    sunrise = int(current['sys']['sunrise'])
    sunrise = add_second_to_unix_time(sunrise, 0)
    sunset = int(current['sys']['sunset'])
    sunset = add_second_to_unix_time(sunset, 0)
    
    # Load the Jinja2 template
    with open("template/weather-widget.html", "r") as template_file:
        template_content = template_file.read()
        jinja_template = Template(template_content)

    # Render the template with dynamic data
    rendered_html = jinja_template.render(
                                    city=city,
                                    country=location['country'],
                                    temperature=current['main']['temp'],
                                    temp_min=current['main']['temp_min'],
                                    temp_max = current['main']['temp_max'],
                                    pressure=current['main']['pressure'],
                                    humidity=current['main']['humidity'],
                                    sunrise=sunrise,
                                    sunset=sunset,
                                    weather_icon=icon,
                                    weather_desc=description)

    # Display the HTML in Streamlit app
    components.html(rendered_html, height=500, scrolling=False)