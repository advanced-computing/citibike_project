
# 🔍 Revisiting the Proposal: Insights & Adjustments

## **Reflections on CitiBike App Improvements**

---

### 🗓️ **Team Review Meeting**

On **March 8, 2025**, our team conducted a thorough review of the CitiBike App. We recognized the progress made but also identified **seven key areas for improvement** to enhance usability, analytical depth, and overall impact.

---

## 📌 **Key Adjustments & Solutions**

### 🔹 **1. Data Inconsistencies**
- **Issue:** Differences in neighborhood names across datasets hindered integration.
- ✅ **Solution:** Standardized all data to **ZIP code level**, ensuring consistency and eliminating manual adjustments.

### 🔹 **2. Improving Poverty Data Accuracy**
- **Issue:** Lack of precise geographic identifiers limited analytical depth.
- ✅ **Solution:** Consolidated **poverty levels by ZIP code** for greater spatial accuracy.

### 🔹 **3. Handling Large Datasets Efficiently**
- **Issue:** Performance issues with large data volumes affecting key functions (`calculate_trip_duration()`, `group_by_station()`).
- ✅ **Solution:** Implemented **SQL-based optimizations (DuckDB & SQLite)** for faster processing.

### 🔹 **4. Enhancing Visualizations for Better Usability**
- **Issue:** Some charts were informative but not user-friendly.
- ✅ **Solution:** Leveraged **advanced Streamlit tools** to improve interactivity and accessibility.

### 🔹 **5. Strengthening Data Narratives with New Visualizations**
- **Issue:** The existing tables lacked depth in illustrating CitiBike-poverty correlations.
- ✅ **Solution:** Added **scatterplots, histograms, and heatmaps** to highlight key trends.

### 🔹 **6. Improving File & Directory Organization**
- **Issue:** The app had too many scattered files, making updates inefficient.
- ✅ **Solution:** Created a structured directory:
  - 📂 `app_data` (Datasets)
  - 🔧 `app_modules` (Functions)
  - 📜 `main_app.py` & `requirements.txt` in root

### 🔹 **7. Optimizing Team Collaboration**
- **Issue:** Irregular work schedules impacted efficiency.
- ✅ **Solution:** Established **weekly fixed meetings (Saturdays, 12:00–2:00 PM)** for synchronized progress.

---

## 🛠️ **Technical Enhancements & Workflow Improvements**

### 📊 **Database Restructuring**
- Initially, we downloaded CitiBike data in **`.xlsx` format** but converted it to **`.csv` and `.db`** for better efficiency.
- While attempting to add **ZIP codes**, we encountered spatial join complexities due to dataset size.
  💡 **Lesson Learned:** Future large-scale geospatial operations require **higher computational resources**.

### 🎯 **Refined Data Visualizations**
After restructuring and cleaning the datasets:
- **📍 Map**: Provides a **clearer insight** into CitiBike station locations in poverty-stricken areas.
- **📊 Histogram**: Highlights CitiBike station distribution across **poverty levels**.
- **📈 Scatterplot**: Demonstrates a **negative correlation** between CitiBike usage and poverty levels.

🔎 **Key Insight:**  
Both **station availability and trip frequency** **decrease** in high-poverty areas, suggesting **transportation inequalities**.

---

## 📌 **Additional Key Insights Identified So Far**

1. **Map Analysis:** CitiBike stations are densely located in close geographic areas, suggesting a consolidated network over the years.
2. **Histogram Observation:** Stations are mostly found in zip codes with **0% to 30%** poverty levels.
3. **Scatterplot Finding:** Many CitiBike trips originate in **0% to 20%** poverty areas, indicating lower bike usage in **20% to 30% poverty zones**, despite a high number of stations.

---

## 🚀 **Next Steps**

We plan to incorporate **two additional datasets** to enhance our analysis:
- **Traffic congestion data**, to analyze how road congestion impacts CitiBike usage.
- **Hospital admission data**, to explore potential correlations between CitiBike usage, accessibility, and public health.

📌 All changes have been **documented in the Streamlit App** under the **"Proposal Adjustments"** tab.

---

🛠 **Next Steps:** Continue refining visualizations and explore deeper policy implications based on our findings.

🛠 **Next Steps:** Continue refining visualizations and explore deeper policy implications based on our findings.
