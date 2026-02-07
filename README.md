# 🌍 AeroGuard — Smart Air Quality & Health Advisory Platform

AeroGuard is a web-based application that helps people **understand air quality in a practical, human-friendly way**.

Instead of only showing AQI numbers, AeroGuard explains **what the air quality means**, **who it affects**, and **how people can respond**. The goal is awareness, clarity, and smarter everyday decisions.

---

## 🚨 Problem Statement

Air quality data is widely available, but:

* AQI values are hard to interpret
* Health impact is rarely explained clearly
* Most tools are generic and non-interactive

As a result, people often ignore air quality until it becomes dangerous.

---

## 💡 What AeroGuard Does

AeroGuard converts real-time air quality data into **clear insights and actionable guidance**.

### Key Features

* **Real-time AQI Monitoring**
  Fetches live air quality data for selected locations using the WAQI API.

* **Health Risk Interpretation**
  Translates AQI values into understandable health risk levels with guidance for:

  * Children
  * Elderly people
  * Individuals with respiratory conditions
  * Healthy adults

* **Interactive Maps & Heatmaps**
  Visualizes pollution levels geographically to compare nearby regions.

* **Exposure Time Suggestions**
  Recommends safer times for outdoor activities based on air quality trends.

* **AQI Trend Prediction (Experimental)**
  Uses basic machine learning techniques to estimate short-term AQI trends for awareness purposes.

* **Clean & Modular UI**
  Simple, responsive interface designed for clarity and usability.

---

## 🧠 What AeroGuard Is Not

* Not a medical diagnostic tool
* Not an official government alert system
* Not guaranteed to predict AQI accurately
* Not a commercial product

AeroGuard is an **educational and awareness-focused project**.

---

## 🏗️ How the System Works

1. User selects a location
2. AQI data is fetched from the WAQI API
3. Data is processed and classified
4. Health risk levels are derived
5. Results are displayed through dashboards, maps, and recommendations

Each part of the system is modular, making the project easy to maintain and extend.

---

## 🧩 Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **API:** World Air Quality Index (WAQI)
* **Visualization:** Folium, Streamlit components
* **Machine Learning:** Scikit-learn (optional module)
* **Deployment:** Streamlit Cloud

---

## 📂 Project Structure

```
aqi_project/
├── app.py              # Main entry point
├── api/                # AQI data fetching
├── models/             # Prediction logic
├── utils/              # Health classification & helpers
├── ui/                 # UI components and views
├── config/             # Configuration files
```

---

## 🚀 Running the Project Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Set your WAQI API token using environment variables before running the app.

---

## 🌱 Future Improvements

* User personalization and profiles
* Notification alerts for poor air quality
* Improved AQI prediction models
* Mobile-friendly interface
* Integration with additional data sources

---

## 🎯 Purpose of This Project

AeroGuard was built as:

* A learning-focused project
* A portfolio-ready application
* A hackathon-usable system
* A real attempt to solve a real-world problem

Clean air affects everyone. Understanding it should be simple.

---

## 📜 License

This project is intended for educational and non-commercial use.

---
## 👥 Contributors

- **[Sachin Kumawat](https://github.com/your-username)** — Project lead, system design, backend & integration  
- **[Karmanya Jakhotia](https://github.com/Karmanya-Jakhotia)** — Frontend UI & Streamlit components   
- **[Rajwardhan Patil](https://github.com/Rajwardhan-09)** — Data analysis & Heatmap
- **[Siddhant Mondkar](https://github.com/AbYsMaL00)** — Documentation, testing and UI Designing

