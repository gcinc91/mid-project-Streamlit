import datetime
import time
import pandas as pd
import streamlit as st
import numpy as np
import os
import requests
import json
import math
from helpers.helper import get_date
import altair as alt
import plotly.figure_factory as ff
from bokeh.plotting import figure
import matplotlib.pyplot as plt

BASE_API = os.getenv('API','http://localhost:5000')

st.markdown(
    """
    <style>
    .reportview-container {
        background: #2A89B9
    }
   .sidebar .sidebar-content {
        background: #2A89B9
    }
    </style>
    """,
    unsafe_allow_html=True
)

# título
st.title("Dashbord Covid-19")

st.header("Evolucion de los paises afectados")


today = st.date_input("Seleccione fecha",datetime.date(2020, 1, 23),datetime.date(2019, 1, 22))
date_selected = get_date(today)
resp = requests.get(f"{BASE_API}/data/fetch-by-date?date={date_selected}")
data_list = json.loads(resp.text)


coordinates = []
for i in data_list:
    if  not math.isnan(i['Lat']) and not math.isnan(i['Long']) and i['confirmed'] > 0:
        coordinates.append([i['Lat'],i['Long']])  


map_data = pd.DataFrame(
    coordinates,
    columns=['lat', 'lon'])

st.map(map_data)


st.header("Datos sobre un pais en concreto")
st.markdown('por defecto se muestran los datos de **argentina**.')

country = st.text_input("Elija pais:") or 'argentina'
country_data = requests.get(f"{BASE_API}/data/fetch/{country}")
info = json.loads(country_data.text) 


cases = []
for i in info:
    cases.append([i['confirmed'],i['deaths'],i['recovered']])

df_info = pd.DataFrame(info,columns=['confirmed', 'deaths', 'recovered','date'])

st.write(df_info)

df = pd.DataFrame(
    cases,
    columns=['confirmed', 'deaths', 'recovered'])

c = alt.Chart(df).mark_circle().encode(
    x='confirmed', y='deaths', size='recovered', color='recovered', tooltip=['confirmed', 'deaths', 'recovered'])

st.write(c)


