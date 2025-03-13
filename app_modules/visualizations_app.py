import plotly.express as px
import pandas as pd

def plot_citibike_poverty_map(poverty_df, geojson_data, zip_code_station_count):
    poverty_df["zipcode"] = poverty_df["zipcode"].astype(str)

    fig = px.choropleth_mapbox(
        poverty_df,
        geojson=geojson_data,
        locations="zipcode",
        featureidkey="properties.ZCTA5CE10",
        color="poverty",
        color_continuous_scale="reds",
        mapbox_style="carto-darkmatter",
        zoom=10,
        center={"lat": 40.7128, "lon": -74.0060},
        opacity=0.7,
        labels={"poverty": "Poverty (%)"}
    )

    max_stations = zip_code_station_count["stations_count"].max()
    zip_code_station_count["marker_size"] = (zip_code_station_count["stations_count"] / max_stations) * 20

    fig.add_scattermapbox(
        lat=zip_code_station_count["start_lat"],
        lon=zip_code_station_count["start_lng"],
        mode="markers",
        marker=dict(
            size=zip_code_station_count["marker_size"],
            color="#0099FF",
            opacity=0.9
        ),
        text=zip_code_station_count["stations_count"].apply(lambda x: f"CitiBike Stations: {x}"),
        hoverinfo="text",
        name="CitiBike Stations by ZIP Code"
    )

    fig.update_layout(
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="white")
    )

    return fig

def plot_poverty_histogram(poverty_df):
    poverty_df["poverty_range_clean"] = poverty_df["poverty_range"].str.replace("%", "")

    poverty_df["hover_text"] = poverty_df["stations_count"].apply(lambda x: f"CitiBike Stations = {x}")

    fig = px.bar(
        poverty_df,
        x="poverty_range_clean",
        y="stations_count",
        color="poverty_range_clean",
        color_discrete_sequence=[
            "#FFD700",
            "#FFA500",
            "#FF8C00",
            "#FF4500",
            "#FF0000"
        ],
        hover_data={"hover_text": True, "poverty_range_clean": False, "stations_count": False},  
        labels={"hover_text": "", "poverty_range_clean": "Poverty (%)"}
    )

    fig.update_layout(
        title="",
        xaxis_title="Poverty (%)",
        yaxis_title="Number of Citibike Stations",
        coloraxis_showscale=False,
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="white")
    )

    return fig

def plot_poverty_scatter(poverty_trips_df):
    print("Min number_of_trips:", poverty_trips_df["number_of_trips"].min())
    print("Max number_of_trips:", poverty_trips_df["number_of_trips"].max())

    fig = px.scatter(
        poverty_trips_df,
        x="poverty",
        y="number_of_trips",
        color="poverty",
        labels={"number_of_trips": "Number of CitiBike Trips", "poverty": "Poverty (%)"},
        template="plotly_dark"
    )

    fig.update_layout(
        paper_bgcolor="black",
        plot_bgcolor="black",
        font=dict(color="white")
    )

    return fig