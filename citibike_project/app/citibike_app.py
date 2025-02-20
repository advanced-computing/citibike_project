import streamlit as st
import pandas as pd
import plotly.express as px
import json
from urllib.request import urlopen

st.title("CitiBike Analysis in Queens")
st.markdown("### App developed by Krishna Kishore and Angel Ragas")

GITHUB_BASE_URL = "https://raw.githubusercontent.com/advanced-computing/citibike_project/main/citibike_project/app/"

st.sidebar.header("Load Data")
load_citibike = st.sidebar.checkbox("Load CitiBike Station Data")
load_poverty = st.sidebar.checkbox("Load CitiBike Concentration Data")

df_bike = None  
df_poverty = None  
geojson_data = None

@st.cache_data
def load_data_from_github(file_name):
    url = GITHUB_BASE_URL + file_name
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Error al cargar {file_name} desde GitHub: {e}")
        return None

@st.cache_data
def load_geojson():
    url = "https://services5.arcgis.com/GfwWNkhOj9bNBqoJ/arcgis/rest/services/NYC_Neighborhood_Tabulation_Areas_2020/FeatureServer/0/query?where=1=1&outFields=*&outSR=4326&f=pgeojson"
    with urlopen(url) as response:
        return json.load(response)

if load_citibike:
    df_bike = load_data_from_github("Queens_citibike.csv")

    if df_bike is not None:
        st.success("CitiBike Station Data for Queens Loaded Successfully")


        possible_lat_names = ["latitude", "start_lat"]
        possible_lng_names = ["longitude", "start_lng"]

        lat_col = next((col for col in df_bike.columns if col in possible_lat_names), None)
        lng_col = next((col for col in df_bike.columns if col in possible_lng_names), None)

        if lat_col and lng_col:
            df_bike.rename(columns={lat_col: "latitude", lng_col: "longitude"}, inplace=True)
            st.subheader("CitiBike Stations Map (Queens)")
            st.map(df_bike[['latitude', 'longitude']])
        else:
            st.error("No se encontraron columnas de latitud y longitud en CitiBike dataset!")


if load_poverty:
    df_poverty = load_data_from_github("new_poverty_data.csv")

    if df_poverty is not None:
        st.success("CitiBike Concentration Data Loaded Successfully")


geojson_data = load_geojson()


if df_bike is not None and df_poverty is not None and geojson_data is not None:
    st.subheader("CitiBike Concentration in Queens")


    df_poverty_queens = df_poverty[df_poverty["State 1"] == "Queens"]


    df_bike_grouped = df_bike.groupby("start_station_name").size().reset_index(name="station_count")
    df_bike_grouped.rename(columns={"start_station_name": "Neighborhood"}, inplace=True)


    df_merged_queens = df_bike_grouped.merge(df_poverty_queens, on="Neighborhood", how="left")
    df_merged_queens.dropna(subset=["Poverty"], inplace=True)


    df_merged_queens["Neighborhood"] = df_merged_queens["Neighborhood"].str.upper()


    for feature in geojson_data["features"]:
        feature["properties"]["Neighborhood"] = feature["properties"].get("Neighborhood", "Unknown").upper()


    df_merged_queens["station_count"].fillna(0, inplace=True)


    df_merged_queens["station_count"] = pd.to_numeric(df_merged_queens["station_count"], errors='coerce').fillna(0)


    fig = px.choropleth_mapbox(
        df_merged_queens,
        geojson=geojson_data,
        locations="Neighborhood",
        featureidkey="properties.Neighborhood",
        color="Poverty",
        color_continuous_scale="Reds",
        range_color=[df_merged_queens["Poverty"].min(), df_merged_queens["Poverty"].max()],
        mapbox_style="carto-positron",
        zoom=10,
        center={"lat": 40.7282, "lon": -73.7949},
        opacity=0.6,
        title="Heatmap of CitiBike Stations Concentration in Queens"
    )


    df_bike_grouped_dict = df_bike_grouped.set_index("Neighborhood")["station_count"].to_dict()
    df_bike["station_count"] = df_bike["start_station_name"].map(df_bike_grouped_dict)


    df_bike["station_count"].fillna(0, inplace=True)

    fig.add_trace(px.scatter_mapbox(
        df_bike,
        lat="latitude",
        lon="longitude",
        size="station_count",
        color_discrete_sequence=["blue"],
        size_max=20,
        hover_name="start_station_name",
        hover_data=["latitude", "longitude", "station_count"]
    ).data[0])


    st.plotly_chart(fig)

import streamlit as st
import pandas as pd
from urllib.request import urlopen


GITHUB_BASE_URL = "https://raw.githubusercontent.com/advanced-computing/citibike_project/main/citibike_project/app/"

st.sidebar.title("Pages")
page = st.sidebar.radio("Select a Page", ["CitiBike Analysis in Queens", "Poverty by Neighborhoods in Queens"])


@st.cache_data
def load_data_from_github(file_name):
    url = GITHUB_BASE_URL + file_name
    try:
        return pd.read_csv(url)
    except Exception as e:
        st.error(f"Error loading {file_name} from GitHub: {e}")
        return None


if page == "Poverty by Neighborhoods in Queens":
    st.title("Poverty Data by Neighborhoods in Queens")


    df_poverty = load_data_from_github("new_poverty_data.csv")
    
    if df_poverty is not None:

        df_poverty_queens = df_poverty[df_poverty["State 1"].str.contains("Queens", case=False, na=False) | 
                                       df_poverty["State 2"].str.contains("Queens", case=False, na=False)]
        

        df_poverty_queens.reset_index(drop=True, inplace=True)
        df_poverty_queens.index += 1
        

        st.write(df_poverty_queens[["Neighborhood", "Poverty"]])
    else:
        st.error("Poverty data not loaded correctly.")