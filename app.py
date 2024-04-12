import random
import numpy as np
import folium
import streamlit as st
from streamlit_folium import st_folium
from folium.plugins import Geocoder, MeasureControl, LocateControl
import plotly.express as px

# My lib
import oweather_api as wapi
import weather_widget as wwidget

# Set up initial map state
DEFAULT_LATITUDE = 16.0544
DEFAULT_LONGITUDE = 108.2022
CENTER_START = [DEFAULT_LATITUDE, DEFAULT_LONGITUDE]
ZOOM_START = 6

st.set_page_config(
    page_title="Python Weather Forecast", 
    page_icon=":rainbow:",
    layout="wide"
)

def initialize_session_state():
    if "center" not in st.session_state:
        st.session_state["center"] = CENTER_START
    if "zoom" not in st.session_state:
        st.session_state["zoom"] = ZOOM_START
    if "markers" not in st.session_state:
        st.session_state["markers"] = []
    if "map_data" not in st.session_state:
        st.session_state["map_data"] = {}
    if "weather_data" not in st.session_state:
        st.session_state["weather_data"] = {}
    # if "all_drawings" not in st.session_state["map_data"]:
    #     st.session_state["map_data"]["all_drawings"] = None
    # if "upload_file_button" not in st.session_state:
    #     st.session_state["upload_file_button"] = False

def reset_session_state():
    # Delete all the items in Session state besides center and zoom
    for key in st.session_state.keys():
        if key in ["center", "zoom"]:
            continue
        del st.session_state[key]
    initialize_session_state()

def initialize_map(center, zoom):
    m = folium.Map(location=center, zoom_start=zoom, scrollWheelZoom=False)
    folium.LatLngPopup().add_to(m)
    LocateControl().add_to(m)
    Geocoder(add_marker=True, collapsed=True, zoom=11).add_to(m)
    MeasureControl(position='bottomleft', primary_length_unit='kilometers',
                   secondary_length_unit='meters', primary_area_unit='sqkilometers', secondary_area_unit='sqmeters').add_to(m)
    return m

initialize_session_state()

weather_map = initialize_map(
    center=st.session_state["center"], zoom=st.session_state["zoom"])

with st.container():
    st.title("FSB Weather Forecast App")
    
    # Buttons
    col1, col2, col3 = st.columns((1,1,4))

    if col1.button("Show Forecast", help="Show Weather Forecast for this location"):
        if 'map_data' in st.session_state:
            try:
                center = st.session_state['map_data']['center']
                st.session_state['weather_data']['current'] = wapi.get_current_forecast(lat=center['lat'], lon=center['lng'])
                st.session_state['weather_data']['future'] = wapi.get_5_days_forecast(lat=center['lat'], lon=center['lng'])
                st.session_state['weather_data']['location'] = wapi.get_geocode_location_info(lat=center['lat'], lon=center['lng'])
            except Exception as e:
                st.warning(e)
                
        # if 'map_data' and 'last_clicked' in st.session_state['map_data']:
        #         last_clicked = st.session_state['map_data']['last_clicked']
        #         if last_clicked is not None:
        #             print(last_clicked)
        #             # st.session_state["markers"] = [
        #             #     folium.Marker(location=[last_clicked['lat'], last_clicked['lng']], popup="Test", icon=folium.Icon(icon='home', prefix='fa', color="red"))]

    if col2.button("Clear Map", help="ℹ️ Click me to **clear the map and reset**"):
        reset_session_state()
        weather_map = initialize_map(
            center=st.session_state["center"], zoom=st.session_state["zoom"])
        
    with col3:
        pass
    
    col_left, col_right = st.columns((8, 6))
    
    with col_left:

        st.caption("Your map")
        
        fg = folium.FeatureGroup(name="Markers")
        for marker in st.session_state["markers"]:
            fg.add_child(marker)
            
        # Create the map and store interaction data inside of session state
        map_data = st_folium(
            weather_map,
            center=st.session_state["center"],
            zoom=st.session_state["zoom"],
            feature_group_to_add=fg,
            key="new",
            width=1285,
            height=725,
            # returned_objects=["all_drawings"],
            use_container_width=True
        )
        
        st.session_state['map_data'] = map_data
        
    with col_right:
        st.caption("Weather")
        
        if 'weather_data' in st.session_state and len(st.session_state['weather_data']) > 0:
            wwidget.draw_weather_forecast(st.session_state['weather_data'])
            
            center = st.session_state['map_data']['center']
            forecast_data = wapi.get_5_days_forecast(lat=center['lat'], lon=center['lng'])
            daily_temps, daily_dates, pressure, humidity = wapi.get_temperatures_date(forecast_data)

            fig_temps = px.line(x=daily_dates, y=daily_temps, title='5-Day Temperature', labels={"x": "Date", "y": "Temperature (°C)"})
            fig_pressure = px.line(x=daily_dates, y=pressure, title='5-Day Pressure', labels={"x": "Date", "y": "Pressure (Mpa)"})
            fig_humidity = px.bar(x=daily_dates, y=humidity, title='5-Day Humidity', labels={"x": "Date", "y": "Humidity (g/m³)"})
            
            st.plotly_chart(fig_temps, use_container_width=True)
            st.plotly_chart(fig_pressure, use_container_width=True)
            st.plotly_chart(fig_humidity, use_container_width=True)
    
    st.write("## session_state")
    st.write(st.session_state)
        