import pandas as pd
import requests

def load_poverty_data():
    return pd.read_excel("https://raw.githubusercontent.com/advanced-computing/citibike_project/main/app_data/poverty_zip_code.xlsx")

def load_geojson():
    response = requests.get("https://raw.githubusercontent.com/advanced-computing/citibike_project/main/app_data/nyc_zipcodes_filtered.geojson")
    return response.json()

def load_citibike_data():
    dtype_dict = {
        "start_station_id": str,
        "zip_code_start": str,
    }
    df_part1 = pd.read_csv("https://raw.githubusercontent.com/advanced-computing/citibike_project/main/app_data/citibike_2022_part_1.csv",
                           usecols=["start_station_id", "start_lat", "start_lng", "zip_code_start", "started_at"],
                           dtype=dtype_dict)
    df_part2 = pd.read_csv("https://raw.githubusercontent.com/advanced-computing/citibike_project/main/app_data/citibike_2022_part_2.csv",
                           usecols=["start_station_id", "start_lat", "start_lng", "zip_code_start", "started_at"],
                           dtype=dtype_dict)
    return pd.concat([df_part1, df_part2], ignore_index=True)

def process_poverty_data(poverty_df, citibike_df):
    poverty_df["zipcode"] = poverty_df["zipcode"].astype(str)
    citibike_df["zip_code_start"] = citibike_df["zip_code_start"].astype(str)

    citibike_df["zip_code_start"] = citibike_df["zip_code_start"].str.split('.').str[0]

    print("Unique ZIP codes in poverty_df:", poverty_df["zipcode"].unique()[:10])
    print("Unique ZIP codes in citibike_df:", citibike_df["zip_code_start"].unique()[:10])

    print("Missing values in poverty_df['zipcode']:", poverty_df["zipcode"].isnull().sum())
    print("Missing values in citibike_df['zip_code_start']:", citibike_df["zip_code_start"].isnull().sum())

    zip_code_station_count = citibike_df.groupby("zip_code_start").agg({
        "start_station_id": "nunique",
        "start_lat": "first",
        "start_lng": "first"
    }).reset_index()

    zip_code_station_count.rename(columns={"start_station_id": "stations_count"}, inplace=True)

    zip_code_station_count = zip_code_station_count.merge(
        poverty_df[["zipcode", "poverty"]],
        left_on="zip_code_start",
        right_on="zipcode",
        how="left"
    )

    zip_code_station_count.drop(columns=["zipcode"], inplace=True)

    print("Columns in zip_code_station_count:", zip_code_station_count.columns)
    print(zip_code_station_count.head())

    poverty_df["stations_count"] = poverty_df["zipcode"].map(
        zip_code_station_count.set_index("zip_code_start")["stations_count"]
    )
    poverty_df["stations_count"] = poverty_df["stations_count"].fillna(0).astype(int)

    bins = [0, 10, 20, 30, 40, 50, 100]
    labels = ["0-10%", "10-20%", "20-30%", "30-40%", "40-50%", "50-100%"]
    poverty_df["poverty_range"] = pd.cut(
        poverty_df["poverty"],
        bins=bins,
        labels=labels
    )

    stations_by_poverty_df = poverty_df.groupby("poverty_range")["stations_count"].sum().reset_index()

    trips_by_zip = citibike_df.groupby("zip_code_start").size().reset_index(name="number_of_trips")
    poverty_trips_df = poverty_df.merge(
        trips_by_zip, left_on="zipcode", right_on="zip_code_start", how="left"
    )
    poverty_trips_df["number_of_trips"] = poverty_trips_df["number_of_trips"].fillna(0).astype(int)

    poverty_trips_df["poverty_range"] = pd.cut(
        poverty_trips_df["poverty"],
        bins=bins,
        labels=labels
    )

    return poverty_df, zip_code_station_count, poverty_trips_df, stations_by_poverty_df