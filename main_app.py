import streamlit as st
from functions_app import load_and_process_data
from tabs_app import display_tabs

merged_data, unique_stations = load_and_process_data()

st.title("CitiBike Analysis in Queens")

display_tabs(merged_data, unique_stations)