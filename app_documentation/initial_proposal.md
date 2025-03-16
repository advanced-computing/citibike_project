
# 📊 Project Proposal

## **Analyzing the Intersection of Citi Bike Usage and Poverty in NYC**

---

### 📂 **Datasets Used**

We are using the following datasets:

1. **Citi Bike Trip Data**: Contains records of bike-sharing trips, including:
   - Start and end times
   - Station locations
   - Trip durations
   - User types  
   📌 [Dataset Link](https://s3.amazonaws.com/tripdata/index.html)

2. **Poverty Map**: Provides real-time and historical traffic speed data, including:
   - % Povery Rate
   - Zip Code 
   🚦 [Dataset Link](https://www.nyc.gov/site/opportunity/poverty-in-nyc/poverty-data.page)

3. **NYC Planning Districts and Boundaries**: Offers geographic boundary information for administrative divisions.  
   🌎 [Dataset Link](https://www.nyc.gov/site/planning/data-maps/open-data/districts-download-metadata.page)

💡 *Initially, we considered the NYCgov Poverty Measure Data (2018), but it lacked location-specific data. We are exploring alternatives like ACS data or proxies such as SNAP participation, Medicaid, and unemployment rates.*

---

### 🔍 **Research Questions**

- How does Citi Bike usage vary across neighborhoods with different poverty?
- What is the relationship (if any) between poverty and Citi Bike trip duration?
- Do high-poverty areas have lower Citi Bike adoption rates?
- Are Citi Bike stations strategically placed to serve high-poverty and congested areas?

---

### 📈 **Target Visualizations**

We aim to use:
- **Interactive Maps** 🗺️ to visualize Citi Bike stations and poverty rates.
- **Histograms** 📊 to show correlations between poverty and bike usage.
- **Scatterplots** 📌 to analyze Citi Bike trip patterns.

---

### 🤔 **Challenges & Known Unknowns**

#### 🔹 **Data Complexity & Integration**
- Different datasets have **varying structures, formats, and update frequencies**.
- Citi Bike data is **trip-based**, traffic data is **segment-based**, and poverty data is **district-level**, which may create **misalignment issues**.

#### 🔹 **Conceptual Definitions**
- How should we define *"Citi Bike adoption rate"*? (Per capita trips, total trips per station, etc.)
- What metric best represents *"Traffic congestion"*? (Average speed, peak-hour congestion, etc.)

#### 🔹 **Technical Issues**
- **Missing values** (e.g., traffic sensor failures, incomplete trip records).
- **Time scale differences**: Citi Bike data is **monthly**, traffic data is **real-time**, and poverty data is **static**.

---

### 🛠️ **Challenges in Policy Interpretation**

Even if we identify patterns, it may be difficult to determine **whether Citi Bike stations were placed to support low-income neighborhoods or congested areas**. Other factors like **commercial interests, political decisions, or budget constraints** might have played a role.

---

### 📌 **Project Notebook**
🔗 [Google Colab Notebook](https://colab.research.google.com/drive/1N8Z-6FjCEXZ_CET-8oCesWf3CIS6maOE#scrollTo=jomMelmueW7L)