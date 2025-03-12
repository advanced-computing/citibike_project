import streamlit as st
import pandas as pd
import os
import plotly.express as px
import json

# 📌 Aplicar fondo oscuro y ajustar colores de texto
st.markdown("""
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .stApp {
            background-color: #121212;
        }
        h1, h2, h3, h4, h5, h6, p, span, div {
            color: white !important;
        }
        .stPlotlyChart {
            background-color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

# 📌 GitHub URL for the citibike CSV files
CITIBIKE_CSV_URL_PART1 = "https://raw.githubusercontent.com/advanced-computing/citibike_project/main/app_data/citibike_2022_part_1.csv"  # Link to the raw file on GitHub
CITIBIKE_CSV_URL_PART2 = "https://raw.githubusercontent.com/advanced-computing/citibike_project/main/app_data/citibike_2022_part_2.csv"  # Link to the raw file on GitHub
POVERTY_XLSX_URL = "https://raw.githubusercontent.com/advanced-computing/citibike_project/main/app_data/poverty_zip_code.xlsx"  # Path to the raw Excel file on GitHub
GEOJSON_URL = "https://raw.githubusercontent.com/advanced-computing/citibike_project/main/app_data/nyc_zipcodes.geojson"  # Path to the raw GeoJSON file on GitHub

# 📌 Function to download files from GitHub if not already in the folder
def download_file_from_github(url, local_file):
    if not os.path.exists(local_file):
        st.info(f"Downloading {local_file} from GitHub...")
        gdown.download(url, local_file, quiet=False)
        st.success(f"Successfully downloaded {local_file}! ✅")

# 📌 Download the necessary files (Poverty and GeoJSON)
download_file_from_github(POVERTY_XLSX_URL, "poverty_zip_code.xlsx")
download_file_from_github(GEOJSON_URL, "nyc_zipcodes.geojson")

# 📌 Load poverty data from Excel
def load_poverty_data():
    return pd.read_excel("poverty_zip_code.xlsx")

# 📌 Load poverty data and GeoJSON
poverty_df = load_poverty_data()

with open("nyc_zipcodes.geojson", "r") as f:
    geojson_data = json.load(f)

# 📌 Load Citi Bike data from GitHub using the raw URL (combining both parts)
citibike_df_part1 = pd.read_csv(CITIBIKE_CSV_URL_PART1, usecols=["start_station_id", "start_lat", "start_lng", "zip_code_start", "started_at"])
citibike_df_part2 = pd.read_csv(CITIBIKE_CSV_URL_PART2, usecols=["start_station_id", "start_lat", "start_lng", "zip_code_start", "started_at"])

# 📌 Merge the two Citi Bike datasets
citibike_df = pd.concat([citibike_df_part1, citibike_df_part2], ignore_index=True)

# 📌 Filter only the ZIP codes of NYC (filtered by GeoJSON, no need for manual filtering here)
geojson_data["features"] = [f for f in geojson_data["features"] if str(f["properties"].get("ZCTA5CE10")) in [f["properties"]["ZCTA5CE10"] for f in geojson_data["features"]]]

# 📌 Group by ZIP Code and count unique stations in each ZIP Code
zip_code_station_count = citibike_df.groupby("zip_code_start").agg({"start_station_id": "nunique", "start_lat": "mean", "start_lng": "mean"}).reset_index()

# 📌 Associate Citi Bike station count with the poverty rate for each ZIP code
poverty_df["stations_count"] = poverty_df["zipcode"].map(zip_code_station_count.set_index("zip_code_start")["start_station_id"])

# 📌 Create poverty ranges for the histogram
bins = [0, 10, 20, 30, 40, 50, 100]
labels = ['0-10%', '10-20%', '20-30%', '30-40%', '40-50%', '50-100%']
poverty_df['poverty_range'] = pd.cut(poverty_df['poverty'], bins=bins, labels=labels)

# 📌 Count how many unique stations are in each poverty range
stations_by_poverty = poverty_df.groupby('poverty_range').agg({'stations_count': 'sum'}).reset_index()

# 📌 Normalize the size of the markers
max_stations = zip_code_station_count["start_station_id"].max()
zip_code_station_count["marker_size"] = zip_code_station_count["start_station_id"] / max_stations * 20  # Scale from 0 to 20

# 📌 Create the map with Plotly
fig = px.choropleth_mapbox(
    poverty_df,
    geojson=geojson_data,
    locations="zipcode",
    featureidkey="properties.ZCTA5CE10",
    color="poverty",
    color_continuous_scale="reds",
    mapbox_style="carto-positron",
    zoom=10,
    center={"lat": 40.7128, "lon": -74.0060},  # Coordinates of New York
    opacity=0.7
)

# 📌 Add a marker per ZIP Code with the number of unique Citi Bike stations
fig.add_scattermapbox(
    lat=zip_code_station_count["start_lat"],
    lon=zip_code_station_count["start_lng"],
    mode="markers",
    marker=dict(
        size=zip_code_station_count["marker_size"],  # Adjusted size of the markers
        color="blue", 
        opacity=0.6
    ),
    text=zip_code_station_count["start_station_id"].apply(lambda x: f"CitiBike Stations: {x}"),
    hoverinfo="text",  # Show the information on hover
    name="CitiBike Stations by ZIP Code"
)

# 📌 Create the histogram based on poverty range
stations_by_poverty = poverty_df.groupby('poverty_range').agg({'stations_count': 'sum'}).reset_index()

fig_histogram = px.bar(stations_by_poverty, 
                       x="poverty_range", 
                       y="stations_count", 
                       color="poverty_range", 
                       color_discrete_map={'0-10%': 'rgb(255, 229, 204)', '10-20%': 'rgb(255, 153, 102)', 
                                           '20-30%': 'rgb(255, 77, 36)', '30-40%': 'rgb(255, 0, 0)', 
                                           '40-50%': 'rgb(204, 0, 0)', '50-100%': 'rgb(139, 0, 0)'}, 
                       title="Number of Citi Bike Stations by Poverty Range",
                       labels={"stations_count": "Number of Stations"},
                       text_auto=False,  # Do not show text on the bars
                       template="plotly_dark",  # Dark background
                       height=500)  # Better size

# 📌 Improve aesthetic, legend, and fonts
fig_histogram.update_layout(
    xaxis_title="Poverty Range",
    yaxis_title="Number of Stations",
    font=dict(size=14),  # Font size
    title_font=dict(size=20, family="Arial, sans-serif", color="white"),
    xaxis=dict(showgrid=False),  # Remove grid lines
    yaxis=dict(showgrid=True, gridcolor='grey'),
    plot_bgcolor="rgb(10,10,10)",  # Dark background for the plot
    paper_bgcolor="rgb(10,10,10)",  # Dark gray background for the entire figure
    margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins
)

# 📌 Create the Scatterplot
# 📌 Count the number of trips for each ZIP code (only start station)
trips_by_zip = citibike_df.groupby("zip_code_start").size().reset_index(name="number_of_trips")

# 📌 Merge the trips data with poverty data
poverty_trips_df = poverty_df.merge(trips_by_zip, left_on="zipcode", right_on="zip_code_start", how="left")

# 📌 Create the scatterplot
fig_scatter = px.scatter(
    poverty_trips_df, 
    x="poverty", 
    y="number_of_trips", 
    color="poverty", 
    color_continuous_scale="reds", 
    labels={"poverty": "Poverty Rate (%)", "number_of_trips": "Number of Trips"},
    title="Scatterplot of Poverty vs. Number of Trips (Start Station)",
    template="plotly_dark"
)

# 📌 Improve aesthetic, legend, and fonts
fig_scatter.update_layout(
    xaxis_title="Poverty Rate (%)",
    yaxis_title="Number of Trips",
    font=dict(size=14),  # Font size
    title_font=dict(size=20, family="Arial, sans-serif", color="white"),
    plot_bgcolor="rgb(10,10,10)",  # Dark background for the plot
    paper_bgcolor="rgb(10,10,10)",  # Dark gray background for the entire figure
    margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins
)

# 📌 Crear pestañas en la barra lateral con letras negras en la selección
st.sidebar.markdown("""
    <style>
        div[role="radiogroup"] label span {
            color: black !important;
        }
    </style>
""", unsafe_allow_html=True)

# 📌 Estilos personalizados para que la selección desplegable sea negra con letras blancas
# 📌 Estilos personalizados barra lateral (fondo negro y letras blancas)
st.sidebar.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            background-color: #121212 !important;
            color: white !important;
        }
        div[data-baseweb="radio"] label {
            color: white !important;
        }
        div[data-baseweb="radio"] div {
            background-color: #121212 !important;
        }
    </style>
""", unsafe_allow_html=True)

# 📌 Crear pestañas en la barra lateral
with st.sidebar:
    st.header("Citibike and Poverty")
    option = st.radio(
        "Select visualization:",
        ("Map", "Histogram", "Scatterplot")
    )

# 📌 Mostrar gráficos según selección
if option == "Map":
    st.plotly_chart(fig)
elif option == "Histogram":
    st.plotly_chart(fig_histogram)
elif option == "Scatterplot":
    st.plotly_chart(fig_scatter)