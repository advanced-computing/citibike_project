import pytest
import pandas as pd

### Defining the functions

## filter by date
def filter_by_date(df, start_date, end_date):
    df['started_at'] = pd.to_datetime(df['started_at'])
    return df[(df['started_at'] >= start_date) & (df['started_at'] <= end_date)]

## calculate trip duration
def calculate_trip_duration(df):
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'])
    df['trip_duration'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60
    return df

## group by
def group_by_station(df):
    return df.groupby('start_station_id').size().reset_index(name='trip_count')

## calculate poverty statistics
def calculate_poverty_statistics(df):
    df['zip_code'] = df['zip_code'].astype(str)  # 🔹 Convierte zip_code a string para evitar errores
    return df.groupby('zip_code')['poverty_rate'].agg(['mean', 'max', 'min']).rename(
        columns={'mean': 'mean_poverty', 'max': 'max_poverty', 'min': 'min_poverty'}
    )

### Defining the tests with pytest
## For this part we have used: https://docs.pytest.org/en/stable/how-to/fixtures.html and
## https://www.testim.io/blog/using-pytest-fixtures/

@pytest.fixture
def sample_citibike_data():
    return pd.DataFrame({
        'started_at': ['2023-01-01 08:00:00', '2023-06-15 08:30:00', '2024-01-01 09:00:00'],
        'ended_at': ['2023-01-01 08:30:00', '2023-06-15 09:00:00', '2024-01-01 10:00:00'],
        'start_station_id': [1, 1, 2],
        'zip_code': ["10001", "10001", "10002"],
        'poverty_rate': [10, 20, 30]
    })

@pytest.mark.parametrize("start_date, end_date, expected_count", [
    ('2023-01-01', '2023-12-31', 2),  # Existing test case
    ('2025-01-01', '2025-12-31', 0)   # Edge case: no data in this range
])
## test for filter by date
def test_filter_by_date(sample_citibike_data, start_date, end_date, expected_count):
    result = filter_by_date(sample_citibike_data, start_date, end_date)
    assert len(result) == expected_count

## test for calculate trip duration
def test_calculate_trip_duration(sample_citibike_data):
    result = calculate_trip_duration(sample_citibike_data)
    assert "trip_duration" in result.columns
    assert result["trip_duration"].iloc[0] == 30.0

## test for group by
def test_group_by_station(sample_citibike_data):
    result = group_by_station(sample_citibike_data)
    assert "trip_count" in result.columns
    assert result.loc[result['start_station_id'] == 1, "trip_count"].values[0] == 2

## test for calculate poverty statistics
def test_calculate_poverty_statistics(sample_citibike_data):
    result = calculate_poverty_statistics(sample_citibike_data)
    assert "mean_poverty" in result.columns
    assert result.loc["10001", "mean_poverty"] == 15.0
    assert result.loc["10002", "mean_poverty"] == 30.0

if __name__ == "__main__":
    pytest.main(["functional_tests.py", "-v"])
