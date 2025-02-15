# 🚲 **Analyzing the Intersection of Citi Bike Usage, Traffic Congestion, and Poverty in NYC**

## 👥 **Team Members**
Krishna Kishore and Angel Ragas

## 📌 **Project Overview**
This project investigates how **Citi Bike usage** varies across **NYC neighborhoods** with different levels of **poverty and traffic congestion**. It aims to identify patterns in **bike-sharing adoption, trip durations, and station placements** in relation to **socioeconomic factors** and **traffic conditions**.

## 🎯 **Research Questions**
- How does Citi Bike usage exhibit different patterns across NYC neighborhoods with varying levels of **poverty and traffic congestion**?
- What type of **relationship** (positive, negative, or none) exists between **poverty levels, traffic congestion, and Citi Bike trip duration**?
- Do neighborhoods with **high levels of poverty and traffic congestion** experience **lower Citi Bike adoption rates**?
- How do **similar traffic congestion patterns** across different **income brackets** affect Citi Bike trip patterns?
- Are Citi Bike stations **strategically located** in areas with **higher levels of poverty and congestion**, providing an **alternative mode of transportation**?
- **Bike usage and traffic speed patterns** within the day.
- Are bikes primarily used where **people live or where they work**?
- Which stations have the **least and most bikes available**? Are there any stations with **consistently low availability**?
- Did the **adoption of congestion pricing** affect **Citi Bike usage and traffic speeds**?

## 📊 **Datasets Used**
The project integrates multiple datasets:

1. **Citi Bike Monthly Trip Data**:  
   - Contains details about bike trips, including **start and end times, station locations, trip durations, and user types**.  
   - **Source:** [Citi Bike Trip Data](https://s3.amazonaws.com/tripdata/index.html)  

2. **NYC DOT Traffic Speeds NBE Dataset**:  
   - Provides **real-time and historical traffic speed data** for road segments across NYC.  
   - **Source:** [DOT Traffic Speeds NBE](https://data.cityofnewyork.us/Transportation/DOT-Traffic-Speeds-NBE/i4gi-tjb9/about_data)  

3. **NYC Department of City Planning’s Districts and Boundaries**:  
   - Defines **community district boundaries, boroughs, and other geographic divisions**.  
   - **Source:** [NYC Planning Open Data](https://www.nyc.gov/site/planning/data-maps/open-data/districts-download-metadata.page)  

4. **NYCgov Poverty Measure Data (2018) (Under Evaluation)**:  
   - While initially considered, this dataset **lacks location-based references beyond the borough level**.  
   - We may use **American Community Survey (ACS) or NYU Furman Center data** for a **more precise poverty measure**.



## 📌 **Setup & Usage Instructions**

### **1️⃣ Clone the Repository**
To get started, clone the repository to your local machine:

```bash
git clone https://github.com/advanced-computing/citibike_project.git
cd citibike_project

### 2️⃣ **Create and Activate a Virtual Environment**
To ensure dependencies are managed properly, create and activate a **virtual environment**.

#### ✅ **For macOS & Linux:**
python3 -m venv .venv
source .venv/bin/activate

#### ✅ **For Windows (Command Prompt):**
python -m venv .venv
.venv\Scripts\activate

### 3️⃣ **Install Dependencies**
After activating your virtual environment, install the required dependencies from requirements.txt:
pip install -r requirements.txt

**Note: The setup section will be continuously updated over time.**