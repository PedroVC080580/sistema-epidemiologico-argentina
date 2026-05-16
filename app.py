import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.express as px

from analysis import load_data
from analysis import total_cases
from analysis import cases_by_pathogen
from analysis import detect_outbreaks

# Configuración
st.set_page_config(
    page_title="Sistema Epidemiológico en Argentina",
    page_icon="🇦🇷",
    layout="wide"
)

# Título
st.title("🇦🇷 Sistema Epidemiológico en Argentina")

st.markdown("""
### Plataforma de vigilancia epidemiológica y análisis de enfermedades infecciosas.
""")

# Cargar datos
data = load_data()

# SIDEBAR
st.sidebar.header("🔎 Filtros")

# Filtro ciudades
cities = st.sidebar.multiselect(
    "Seleccionar Ciudad",
    options=data['City'].unique(),
    default=data['City'].unique()
)

# Filtro patógenos
pathogens = st.sidebar.multiselect(
    "Seleccionar Patógeno",
    options=data['Pathogen'].unique(),
    default=data['Pathogen'].unique()
)

# Filtrar datos
filtered_data = data[
    (data['City'].isin(cities)) &
    (data['Pathogen'].isin(pathogens))
]

# Métricas
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Casos", filtered_data['Cases'].sum())

with col2:
    st.metric("Ciudades", filtered_data['City'].nunique())

with col3:
    st.metric("Patógenos", filtered_data['Pathogen'].nunique())

st.divider()

# Tabla
st.subheader("📊 Datos Epidemiológicos")
st.dataframe(filtered_data, use_container_width=True)

st.divider()

# Gráfico dinámico
st.subheader("📈 Casos por Patógeno")

cases = filtered_data.groupby('Pathogen')['Cases'].sum()

fig, ax = plt.subplots(figsize=(8,5))

ax.bar(cases.index, cases.values)

ax.set_xlabel("Patógeno")
ax.set_ylabel("Casos")
ax.set_title("Distribución de Casos")

st.pyplot(fig)

st.divider()

# Detección de brotes
st.subheader("⚠️ Alertas Epidemiológicas")

outbreaks = filtered_data[filtered_data['Cases'] > 50]

if len(outbreaks) > 0:
    st.error("Posibles brotes detectados")
    st.dataframe(outbreaks, use_container_width=True)
else:
    st.success("No se detectaron brotes")
    
st.subheader("🗺️ Mapa Epidemiológico")

city_cases = filtered_data.groupby('City')['Cases'].sum().reset_index()

fig_map = px.bar(
    city_cases,
    x='City',
    y='Cases',
    color='Cases',
    title='Casos por Ciudad'
)

st.plotly_chart(fig_map, use_container_width=True)

st.divider()

st.subheader("🗺️ Mapa Epidemiológico de Argentina")

map_data = filtered_data.groupby(
    ['City', 'Latitude', 'Longitude']
)['Cases'].sum().reset_index()

fig_map = px.scatter_mapbox(
    map_data,
    lat='Latitude',
    lon='Longitude',
    size='Cases',
    color='Cases',
    hover_name='City',
    hover_data=['Cases'],
    zoom=3.5,
    height=600
)

fig_map.update_layout(
    mapbox_style='open-street-map',
    margin={"r":0,"t":0,"l":0,"b":0}
)

st.plotly_chart(fig_map, use_container_width=True)