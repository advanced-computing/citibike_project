import streamlit as st
import pandas as pd
import plotly.express as px
import folium

def display_tabs(merged_data, unique_stations):
    tabs = ["Information", "Citi Bike trips and Poverty", "Citi Bike stations and Poverty", "Map of Citi Bike Stations"]
    selected_tab = st.sidebar.radio("Select a tab:", tabs)

    if selected_tab == "Information":
        st.header("Welcome to the Citi Bike App made by Krishna and Angel")

    elif selected_tab == "Citi Bike trips and Poverty":
        st.header("Number of Trips by Poverty Rate")
        poverty_bins = pd.cut(merged_data['poverty_rate'], bins=range(0, 101, 10), right=False, labels=[str(i) for i in range(0, 100, 10)])
        trip_counts = merged_data.groupby(poverty_bins).size().reset_index(name='trip_count')
        fig1 = px.bar(trip_counts, x='poverty_rate', y='trip_count', labels={'poverty_rate': 'Poverty Rate (%)', 'trip_count': 'Number of Trips'})
        st.plotly_chart(fig1)

    elif selected_tab == "Citi Bike stations and Poverty":
        st.header("CitiBike Stations by Poverty Rate")
        unique_station_counts = unique_stations.groupby(pd.cut(unique_stations['poverty_rate'], bins=range(0, 101, 10), right=False, labels=[str(i) for i in range(0, 100, 10)]))['start_station_id'].nunique().reset_index(name='unique_stations')
        fig2 = px.bar(unique_station_counts, x='poverty_rate', y='unique_stations', labels={'poverty_rate': 'Poverty Rate (%)', 'unique_stations': 'Unique CitiBike Stations'})
        st.plotly_chart(fig2)

    elif selected_tab == "Map of Citi Bike Stations":
        st.header("Map of CitiBike Stations")
        map_center = [unique_stations['start_lat'].astype(float).mean(), unique_stations['start_lng'].astype(float).mean()]
        m = folium.Map(location=map_center, zoom_start=12)
        for _, row in unique_stations.iterrows():
            folium.CircleMarker(
                location=[float(row['start_lat']), float(row['start_lng'])],
                radius=2,
                color='blue',
                fill=True,
                fill_color='blue',
                fill_opacity=0.6
            ).add_to(m)
        st.components.v1.html(m._repr_html_(), height=600)