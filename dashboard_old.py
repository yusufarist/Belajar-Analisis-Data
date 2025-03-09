import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Dashboard Analisis Data", page_icon='assets/Logo.png', layout="wide")
st.logo('assets/Logo Long.png', icon_image='assets/Logo Long.png')

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if 'sampled_dataset' not in st.session_state:
    st.session_state.sampled_dataset = False
    st.session_state.clicked_sample_data = False
if 'filtered_dataset' not in st.session_state:
    st.session_state.filtered_dataset = False
if 'clicked_button_data' not in st.session_state:
    st.session_state.clicked_button_data = False 

data_dashboard = pd.read_csv('main_data.csv')


data_dashboard['dteday'] = pd.to_datetime(data_dashboard['dteday']) # type: ignore

daily_avg_temp = data_dashboard.groupby('dteday')['temp'].mean() # type: ignore
daily_max_hum = data_dashboard.groupby('dteday')['hum'].max() # type: ignore
daily_avg_windspeed = data_dashboard.groupby('dteday')['windspeed'].mean() # type: ignore
daily_avg_casual = data_dashboard.groupby('dteday')['casual'].mean() # type: ignore

delta_temp = daily_avg_temp.diff().iloc[-1]
delta_hum = daily_max_hum.diff().iloc[-1]
delta_windspeed = daily_avg_windspeed.diff().iloc[-1]
delta_casual = daily_avg_casual.diff().iloc[-1]

avg_temp = daily_avg_temp.iloc[-1]
max_hum = daily_max_hum.iloc[-1]
avg_windspeed = daily_avg_windspeed.iloc[-1]
avg_casual = daily_avg_casual.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

with col1.container(border=True):
    st.metric("Rata-Rata Suhu (°C)", f"{avg_temp:.2f}", delta=f"{delta_temp:.2f} °C", delta_color="normal") 

with col2.container(border=True):
    st.metric("Kelembapan Maksimum (%)", f"{max_hum:.2f}", delta=f"{delta_hum:.2f} %") 

with col3.container(border=True):
    st.metric("Rata-Rata Kecepatan Angin (km/h)", f"{avg_windspeed:.2f}", delta=f"{delta_windspeed:.2f} km/h") 

with col4.container(border=True):
    st.metric("Rata-Rata Pengguna Casual", f"{avg_casual:.2f}", delta=f"{delta_casual:.2f}") 

fig = px.line(data_dashboard,
            x="dteday", 
            y="cnt", 
            color="yr", 
            title="Tren Jumlah Peminjaman Sepeda",
            color_discrete_sequence=["#7375b6", "#39a1b1"]) 

st.plotly_chart(fig)

avg_rentals_per_season = data_dashboard.groupby("season")["cnt"].mean() # type: ignore

st.bar_chart(avg_rentals_per_season)

daily_rentals = data_dashboard.groupby('dteday')['cnt'].sum() # type: ignore
st.area_chart(daily_rentals)


hourly_avg = data_dashboard.groupby('hr')['cnt'].mean() # type: ignore
st.bar_chart(hourly_avg)


st.line_chart(data_dashboard[['temp', 'cnt']]) # type: ignore


st.scatter_chart(data_dashboard[['temp', 'cnt']]) # type: ignore


import plotly.express as px
fig = px.scatter(data_dashboard, x='temp', y='cnt', color='hum', size='windspeed', hover_data=['temp', 'cnt', 'hum'])
st.plotly_chart(fig)