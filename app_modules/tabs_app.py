import streamlit as st
from app_modules.visualizations_app import plot_citibike_poverty_map, plot_poverty_histogram, plot_poverty_scatter

def citibike_poverty_tab(poverty_df, geojson_data, zip_code_station_count, poverty_trips_df, stations_by_poverty_df):

    tab1, tab2, tab3 = st.tabs(["Map", "Histogram", "Scatterplot"])

    with tab1:
        st.header("CitiBike Stations and Poverty Map")
        st.plotly_chart(plot_citibike_poverty_map(poverty_df, geojson_data, zip_code_station_count))

    with tab2:
        st.header("CitiBike Stations by Poverty Level")
        st.plotly_chart(plot_poverty_histogram(stations_by_poverty_df))

    with tab3:
        st.header("Poverty vs Number of Trips")
        st.plotly_chart(plot_poverty_scatter(poverty_trips_df))