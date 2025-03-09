import pandas as pd
import streamlit as st
import plotly.express as px

# Konfigurasi dashboard
st.set_page_config(page_title="Dashboard Analisis Data", page_icon='assets/Logo.png', layout="wide")
st.logo('assets/Logo Long.png', icon_image='assets/Logo Long.png')

# **Deskripsi Dashboard**
st.sidebar.caption("""
    Dashboard ini menyajikan analisis tren peminjaman sepeda berdasarkan berbagai faktor seperti suhu, kelembapan, dan musim. 
    """)

# Tambahan di Sidebar
with st.sidebar.container(border=True):
    st.header("ℹ️ Informasi")
    st.markdown("""
    **Sumber Data:** Bike Sharing Dataset  
    **Periode Data:** 2011 - 2012
    """)

# Load Data
data_dashboard = pd.read_csv('main_data.csv')

# Konversi kolom tanggal ke format datetime
data_dashboard['dteday'] = pd.to_datetime(data_dashboard['dteday'])

# Tambahkan kolom hari dalam seminggu
data_dashboard['weekday'] = data_dashboard['dteday'].dt.day_name()

with st.sidebar.container(border=True):
    # Filter berdasarkan tanggal
    st.header("🗓️ Filter Data")
    start_date = st.date_input("Pilih Tanggal Awal", data_dashboard['dteday'].min())
    end_date = st.date_input("Pilih Tanggal Akhir", data_dashboard['dteday'].max())

    if start_date > end_date:
        st.error("Tanggal awal tidak boleh lebih besar dari tanggal akhir.")

    # Terapkan filter tanggal
    filtered_data = data_dashboard[(data_dashboard['dteday'] >= pd.to_datetime(start_date)) & 
                               (data_dashboard['dteday'] <= pd.to_datetime(end_date))]

    st.divider()

    # Filter Season (Opsional)
    season_map = {1: "Winter", 2: "Spring", 3: "Summer", 4: "Fall"}
    filtered_data['season_label'] = filtered_data['season'].map(season_map)

    selected_season = st.selectbox("Pilih Musim", ["Semua"] + list(season_map.values()))
    if selected_season != "Semua":
        filtered_data = filtered_data[filtered_data["season_label"] == selected_season]
        
    st.divider()

    # Filter Cuaca (Opsional)
    weather_map = {1: "Cerah", 2: "Berawan", 3: "Hujan Ringan", 4: "Hujan Lebat"}
    filtered_data['weather_label'] = filtered_data['weathersit'].map(weather_map)

    selected_weather = st.selectbox("Pilih Cuaca", ["Semua"] + list(weather_map.values()))
    if selected_weather != "Semua":
        filtered_data = filtered_data[filtered_data["weather_label"] == selected_weather]
        
    st.divider()

    # Filter Hari dalam Seminggu
    selected_day = st.multiselect("Pilih Hari", options=data_dashboard['weekday'].unique(), default=data_dashboard['weekday'].unique())
    filtered_data = filtered_data[filtered_data["weekday"].isin(selected_day)]

daily_avg_temp = data_dashboard.groupby('dteday')['temp'].mean()
daily_max_hum = data_dashboard.groupby('dteday')['hum'].max()
daily_avg_windspeed = data_dashboard.groupby('dteday')['windspeed'].mean()
daily_avg_casual = data_dashboard.groupby('dteday')['casual'].mean()

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
    
st.divider()

with st.container(border=True):
    # **Visualisasi Data dengan Tabs**
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Tren Peminjaman", "🌦️ Peminjaman per Musim", "📊 Peminjaman per Hari", "☀️ Suhu vs Peminjaman"])

    with tab1:
        st.subheader("📈 Tren Jumlah Peminjaman Sepeda")
        st.markdown("Grafik ini menunjukkan jumlah peminjaman sepeda berdasarkan rentang tanggal yang dipilih.")
        with st.container(border=True):
            fig = px.line(filtered_data, x="dteday", y="cnt", color="yr", 
                        labels={"cnt": "Jumlah Peminjaman", "dteday": "Tanggal", "yr": "Tahun"},
                        color_discrete_sequence=["#FF6347", "#77DD77"])
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        st.markdown("Tren peminjaman sepeda menunjukkan pola musiman dengan lonjakan pada periode tertentu. Peminjaman meningkat pada musim panas dan cenderung menurun saat musim dingin, kemungkinan karena faktor cuaca.")

    with tab2:
        st.subheader("🌦️ Rata-Rata Peminjaman Sepeda per Musim")
        st.markdown("Bagaimana musim memengaruhi jumlah peminjaman sepeda? Grafik ini menunjukkan rata-rata peminjaman berdasarkan musim.")
        with st.container(border=True):
            avg_rentals_per_season = filtered_data.groupby("season_label")["cnt"].mean().reset_index()
            fig_season = px.bar(avg_rentals_per_season, x="season_label", y="cnt", color="season_label",
                                labels={"cnt": "Rata-Rata Peminjaman", "season_label": "Musim"},
                                color_discrete_map={"Winter": "#FFFFFF", "Spring": "#77DD77", "Summer": "#FF6347", "Fall": "#FF8C00"})
            fig_season.update_layout(showlegend=False)
            st.plotly_chart(fig_season, use_container_width=True)
        st.markdown("Musim berpengaruh signifikan terhadap jumlah peminjaman. Musim panas dan musim semi cenderung memiliki lebih banyak peminjaman dibandingkan musim dingin, menunjukkan bahwa faktor cuaca sangat mempengaruhi minat masyarakat dalam menggunakan sepeda.")

    with tab3:
        st.subheader("📊 Distribusi Peminjaman Sepeda per Hari")
        st.markdown("Visualisasi ini menunjukkan pola peminjaman sepeda berdasarkan hari dalam seminggu.")
        with st.container(border=True):
            avg_rentals_per_weekday = filtered_data.groupby("weekday")["cnt"].mean().reset_index()
            # Hitung rentang warna berdasarkan jumlah peminjaman
            min_cnt = avg_rentals_per_weekday["cnt"].min()
            max_cnt = avg_rentals_per_weekday["cnt"].max()
            avg_rentals_per_weekday["color_intensity"] = (avg_rentals_per_weekday["cnt"] - min_cnt) / (max_cnt - min_cnt)
            
            # Warna dari gelap ke terang berdasarkan intensitas
            fig_weekday = px.bar(avg_rentals_per_weekday, x="weekday", y="cnt", 
                                labels={"cnt": "Rata-Rata Peminjaman", "weekday": "Hari"},
                                color="cnt", color_continuous_scale=["#FF6347", "#77DD77"])
            fig_weekday.update_layout(showlegend=False)
            st.plotly_chart(fig_weekday, use_container_width=True)
        st.markdown("Hari kerja dan akhir pekan mempengaruhi jumlah peminjaman sepeda secara signifikan. Peminjaman cenderung lebih tinggi pada hari kerja saat orang bepergian untuk bekerja atau sekolah, sementara akhir pekan menunjukkan pola yang lebih bervariasi.")

    with tab4:
        st.subheader("☀️ Hubungan Suhu dan Peminjaman Sepeda")
        st.markdown("Scatter plot ini menggambarkan hubungan antara suhu dan jumlah peminjaman sepeda.")
        with st.container(border=True):
            fig_temp = px.scatter(filtered_data, x="temp", y="cnt",
                                labels={"temp": "Suhu (°C)", "cnt": "Jumlah Peminjaman"},
                                color="cnt", color_continuous_scale=["#FF6347", "#77DD77"])
            fig_temp.update_layout(showlegend=False)
            st.plotly_chart(fig_temp, use_container_width=True)
        st.markdown("Semakin tinggi suhu, jumlah peminjaman cenderung meningkat, menunjukkan bahwa orang lebih suka bersepeda dalam cuaca hangat. Namun, pada suhu ekstrem, jumlah peminjaman dapat berkurang, kemungkinan karena faktor kenyamanan dan keamanan.")

# Tambahkan CSS untuk mengurangi margin divider
st.markdown("""
    <style>
        hr {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
        }
        h2 {
            margin-top: -10px !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            display: flex;
            justify-content: left;
            gap: 2px;
            width: 100%;
        }

        .stTabs [data-baseweb="tab"] {
            flex: 1; 
            height: 50px;
            border-radius: 4px 4px 0px 0px;
            gap: 25px;
            padding-top: 5px;
            padding-bottom: 10px;
            text-align: center;
            position: relative; 
            font-size: 18px;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)
