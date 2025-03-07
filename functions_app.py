import pandas as pd
import requests
from io import StringIO

def load_data_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        df = pd.read_csv(StringIO(response.text), dtype=str, low_memory=False)
        if df.empty:
            raise ValueError(f"The file at {url} is empty.")
        return df
    else:
        raise ValueError(f"Failed to fetch data from {url}. Status code: {response.status_code}")

def load_and_process_data():
    citibike_url = "https://raw.githubusercontent.com/advanced-computing/citibike_project/main/Queens_citibike.csv"
    poverty_url = "https://raw.githubusercontent.com/advanced-computing/citibike_project/main/poverty_zipcode.csv"
    
    queens_citibike = load_data_from_github(citibike_url)
    poverty_zipcode = load_data_from_github(poverty_url)
    
    queens_citibike = queens_citibike.dropna(subset=['zipcode', 'start_lat', 'start_lng', 'start_station_id'])
    queens_citibike['zipcode'] = queens_citibike['zipcode'].astype(int)
    poverty_zipcode['zipcode'] = poverty_zipcode['zipcode'].astype(int)
    poverty_zipcode.rename(columns={'%': 'poverty_rate'}, inplace=True)
    poverty_zipcode['poverty_rate'] = poverty_zipcode['poverty_rate'].str.replace(',', '.').astype(float)
    
    merged_data = queens_citibike.merge(poverty_zipcode[['zipcode', 'poverty_rate']], on='zipcode', how='left')
    unique_stations = merged_data.drop_duplicates(subset=['start_station_id'])
    
    return merged_data, unique_stations
