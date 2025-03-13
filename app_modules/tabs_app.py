import streamlit as st
from visualizations_app import plot_citibike_poverty_map, plot_poverty_histogram, plot_poverty_scatter

# 📌 Pestaña de CitiBike y Pobreza
def citibike_poverty_tab(poverty_df, geojson_data, zip_code_station_count, poverty_trips_df, stations_by_poverty_df):
    """Muestra la pestaña de CitiBike y Pobreza con un mapa, un histograma y un scatterplot."""

    tab1, tab2, tab3 = st.tabs(["Map", "Histogram", "Scatterplot"])

    with tab1:
        st.header("CitiBike Stations and Poverty Map")
        st.plotly_chart(plot_citibike_poverty_map(poverty_df, geojson_data, zip_code_station_count))

    with tab2:
        st.header("CitiBike Stations by Poverty Level")
        st.plotly_chart(plot_poverty_histogram(stations_by_poverty_df))  # ✅ Se usa el DF específico

    with tab3:
        st.header("Poverty vs Number of Trips")
        st.plotly_chart(plot_poverty_scatter(poverty_trips_df))  # ✅ Se usa el DF específico