import streamlit as st
from app_modules.functions_app import load_poverty_data, load_citibike_data, load_geojson, process_poverty_data
from app_modules.tabs_app import citibike_poverty_tab, show_initial_proposal, show_revisited_proposal
from app_modules.styles_app import apply_styles

apply_styles()

def welcome_tab():
    st.title("🚲 **Welcome to CitiBike App**")
    st.markdown("""
        ### **Project Overview**
        The CitiBike App is designed to analyze CitiBike usage, stations and poverty levels in New York City. 
        It provides interactive visualizations to explore the relationship between public bike stations and socio-economic conditions.
        You are welcome to navigate through this App and interact with our more important visualizations:

        - 📌 **Interactive Map:** Explore CitiBike stations and their distribution across NYC.
        - 📊 **Histogram:** View the correlation between poverty levels and bike stations.
        - 📈 **Scatterplot:** Analyze the relationship between poverty rates and the number of trips.

        ---
        ## 👨‍💻 Developed by:
        ### **Angel Ragas & Krishna Kishore**
        ---
    """)
    st.info("Use the sidebar to navigate through different analysis tabs.")

selected_tab = st.sidebar.radio(
    "Select Analysis",
    ["Welcome", "Citibike and Poverty", "Initial Proposal", "Revisited Proposal"],
    index=0
)

poverty_df = load_poverty_data()
citibike_df = load_citibike_data()
geojson_data = load_geojson()

poverty_df, zip_code_station_count, poverty_trips_df, stations_by_poverty_df = process_poverty_data(poverty_df, citibike_df)

if selected_tab == "Welcome":
    welcome_tab()
elif selected_tab == "Citibike and Poverty":
    citibike_poverty_tab(poverty_df, geojson_data, zip_code_station_count, poverty_trips_df, stations_by_poverty_df)
elif selected_tab == "Initial Proposal":
    show_initial_proposal()
elif selected_tab == "Revisited Proposal":
    show_revisited_proposal()
