**Unit Testing Plan for Citi Bike & Poverty Data Processing**

## **1️⃣ Review Existing Code**

We broke out the code into three different files—main_app.py, functions_app.py, and tabs_app.py—to improve the maintainability and organization of our CitiBike Data Analysis app. While functions_app.py manages data loading and processing, tabs_app.py maintains the UI components, this modular design guarantees that the main script—main_app.py—focusses just on user interaction. Separating issues helps us to reduce needless complication in the main application logic and increase code readability.

This architecture reduces duplication by centralizing common chores such data collection, visualization, and processing into reusable functions using the DRY (Don't Repeat Yourself) concept. The primary script used to include visualization logic for several charts used to result in repeated code. By means of this restructuring, all required modifications—such as changing data sources or revising chart styles—can be made under functions_app.py, therefore avoiding the need to edit several main_app.py sections.

Furthermore enhanced by this modular architecture are testability and scalability. Keeping functions separate allows us to independently evaluate data processing and visualization outputs using unit tests—e.g., with pytest—without affecting the Streamlit UI. Whether by adding new visualizations, including other datasets, or enhancing the interactive components, this framework also facilitates expansion of the program. All things considered, separating the code into separate files has expedited our development process and improved the application's efficiency, organization, and future-proofness.


## **2️⃣ Functions, Test Cases & Expected Outputs**

These functional tests validate **data processing and transformation operations**.

### **Function 1: ****`filter_by_date(df, start_date, end_date)`**

**Objective:** Filters Citi Bike visits depending on a given date period.
**Where can we make our code DRY?** Filtering Citi Bike trips by date should help to stop scattered `df[df['date']...]` operations all throughout the code.

✅ **Test Cases:**

- **Input:** `filter_by_date(test_citibike_df, '2023-01-01', '2023-12-31')`
- **Expected Output:** Returns a `DataFrame` containing only trips within the given date range.

### **Function 2: ****`calculate_trip_duration(df)`**

**Objective:** Calculates trip durations in minutes from `started_at` and `ended_at` columns.
**Where can we make our code DRY?** One can abstract the computation of the trip length into a function to guarantee consistent calculations over datasets free from duplicate timestamp adjustments.

✅ **Test Cases:**

- **Input:** `calculate_trip_duration(pd.DataFrame({'started_at': ['2023-01-01 08:00:00'], 'ended_at': ['2023-01-01 08:30:00']}))`
- **Expected Output:** Returns a `DataFrame` with a new `trip_duration` column containing `30.0` minutes.

### **Function 3: ****`group_by_station(df)`**

**Objective:** Groups Citi Bike trips by `start_station_id` and counts trips per station.
**Where can we make our code DRY?** Aggregating trip counts by station should help to prevent repeated groupby operations distributed in several analyses.

✅ **Test Cases:**

- **Input:** `group_by_station(test_citibike_df)`.
- **Expected Output:** Returns a `DataFrame` grouped by `start_station_id`, showing the count of trips per station.

### **Function 4: ****`calculate_poverty_statistics(df)`**

**Objective:** Calculates, for each Zip code, mean, max, and min poverty rates based on Citi Bike travels.
**Where can we make our code DRY?** To simplify statistical aggregating and prevent repeated computation, the computation of mean, max, and min poverty rates per ZIP code should be consolidated in a function.

✅ **Test Cases:**

- **Input:** `calculate_poverty_statistics(test_citibike_df)`.
- **Expected Output:** Returns a `DataFrame` with columns for mean, max, and min poverty rates per ZIP code.