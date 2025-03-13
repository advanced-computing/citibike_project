import pandas as pd
import requests

# 📌 Funciones de carga de datos
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

# 📌 Procesamiento de datos para CitiBike y pobreza
def process_poverty_data(poverty_df, citibike_df):
    # 🚩 Asegurarse de que las columnas de códigos postales estén en el mismo formato
    poverty_df["zipcode"] = poverty_df["zipcode"].astype(str)
    citibike_df["zip_code_start"] = citibike_df["zip_code_start"].astype(str)

    # 🚩 Normalizar zip_code_start para que coincida con el formato de poverty_df
    citibike_df["zip_code_start"] = citibike_df["zip_code_start"].str.split('.').str[0]

    # 🚩 Comprobar valores únicos de ZIP codes en ambos DataFrames
    print("Unique ZIP codes in poverty_df:", poverty_df["zipcode"].unique()[:10])
    print("Unique ZIP codes in citibike_df:", citibike_df["zip_code_start"].unique()[:10])

    # 🚩 Verificar si hay valores nulos en las columnas clave
    print("Missing values in poverty_df['zipcode']:", poverty_df["zipcode"].isnull().sum())
    print("Missing values in citibike_df['zip_code_start']:", citibike_df["zip_code_start"].isnull().sum())

    # 🚩 Calcular estaciones únicas por ZIP Code
    zip_code_station_count = citibike_df.groupby("zip_code_start").agg({
        "start_station_id": "nunique",
        "start_lat": "first",
        "start_lng": "first"
    }).reset_index()

    zip_code_station_count.rename(columns={"start_station_id": "stations_count"}, inplace=True)

    # 🚩 Verificar algunos datos de `zip_code_station_count`
    print("Zip Code Station Count (first rows):")
    print(zip_code_station_count.head())

    # 🚩 Verificar el mapeo de un ejemplo
    example_zip = poverty_df["zipcode"].iloc[0]
    print("Example ZIP code:", example_zip)
    print("Stations count for example ZIP code:",
          zip_code_station_count.set_index("zip_code_start")["stations_count"].get(example_zip, "Not found"))

    # 🚩 Asociar número de estaciones con la pobreza por ZIP Code
    poverty_df["stations_count"] = poverty_df["zipcode"].map(
        zip_code_station_count.set_index("zip_code_start")["stations_count"]
    )
    poverty_df["stations_count"] = poverty_df["stations_count"].fillna(0).astype(int)

    # 🚩 Crear `poverty_range` para el histograma
    bins = [0, 10, 20, 30, 40, 50, 100]
    labels = ["0-10%", "10-20%", "20-30%", "30-40%", "40-50%", "50-100%"]
    poverty_df["poverty_range"] = pd.cut(
        poverty_df["poverty"],
        bins=bins,
        labels=labels
    )

    # 🚩 Calcular datos para el histograma
    stations_by_poverty_df = poverty_df.groupby("poverty_range")["stations_count"].sum().reset_index()

    # 🚩 Para el scatterplot, no se agrupan viajes, se mantienen los datos originales
    trips_by_zip = citibike_df.groupby("zip_code_start").size().reset_index(name="number_of_trips")
    poverty_trips_df = poverty_df.merge(
        trips_by_zip, left_on="zipcode", right_on="zip_code_start", how="left"
    )
    poverty_trips_df["number_of_trips"] = poverty_trips_df["number_of_trips"].fillna(0).astype(int)

    # 🚩 Asegurarse de que `poverty_range` esté correctamente asociado
    poverty_trips_df["poverty_range"] = pd.cut(
        poverty_trips_df["poverty"],
        bins=bins,
        labels=labels
    )

    # 🚩 Verificar los datos generados (nuevas líneas para revisar los valores antes de graficar)
    print("Stations by Poverty Range:")
    print(stations_by_poverty_df.head())
    print("Poverty Trips Data:")
    print(poverty_trips_df.head())

    return poverty_df, zip_code_station_count, poverty_trips_df, stations_by_poverty_df