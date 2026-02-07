"""
Dashboard view page
"""
import streamlit as st
import plotly.graph_objects as go
from api.waqi_client import WAQIClient
from models.predictor import AQIPredictor
from utils.health_classifier import HealthClassifier


def render_dashboard():
    """Render the dashboard page"""
    
    st.title("🌍 Air Quality Dashboard")
    st.caption("Real-time AQI monitoring, forecasting, and health risk assessment")
    
    # Navigation buttons
    col_nav1, col_nav2, col_nav3, col_nav4 = st.columns([1, 1, 1, 3])
    with col_nav1:
        if st.button("🏠 Home", use_container_width=True):
            st.query_params.update({"action": "home"})
            st.session_state.view = "home"
            st.rerun()
    with col_nav2:
        if st.button("📅 Scheduler", use_container_width=True):
            st.query_params.update({"action": "scheduler"})
            st.session_state.view = "scheduler"
            st.rerun()
    with col_nav3:
        if st.button("🗺️ Heatmap", use_container_width=True):
            st.query_params.update({"action": "heatmap"})
            st.session_state.view = "heatmap"
            st.rerun()
    
    st.markdown("---")
    
    # Initialize client
    client = WAQIClient()
    
    # Search location
    st.markdown("## 📍 Select Location")
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    
    with st.form(key="dashboard_search_form"):
        search_query = st.text_input(
            "Enter city or location",
            placeholder="e.g., Delhi, Mumbai, Bangalore",
            help="Press Enter to search"
        )
        search_btn = st.form_submit_button("🔍 Search Location", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if search_btn and search_query.strip():
        with st.spinner("🔍 Fetching air quality data..."):
            results, err = client.search_places(search_query)
        
        if err or not results:
            st.error("❌ Could not find location. Please try another search term.")
        else:
            # Use first result
            first = results[0]
            aqi_data, err = client.get_feed_by_uid(int(first["uid"]))
            
            if err:
                st.error(f"❌ Error fetching data: {err}")
            else:
                st.session_state.dashboard_data = aqi_data
                st.session_state.dashboard_location = first['name']
                st.success(f"✅ Data loaded for {first['name']}")
    
    # Display dashboard
    if st.session_state.dashboard_data:
        data = st.session_state.dashboard_data
        aqi = data.get("aqi")
        pm25 = data.get("pm25")
        city = data.get("city") or st.session_state.dashboard_location
        
        st.markdown(f"### 📊 Current Status: {city}")
        st.caption(f"Last updated: {data.get('time', 'N/A')}")
        
        # Main metrics
        m1, m2, m3, m4 = st.columns(4)
        
        with m1:
            epa_cat, epa_color, epa_desc, _ = HealthClassifier.get_epa_category(aqi)
            st.markdown('<div class="m-label">💨 Current AQI</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="m-value" style="color:{epa_color};">{aqi if aqi else "N/A"}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="m-sub">{epa_cat}</div>', unsafe_allow_html=True)
        
        with m2:
            who_cat, who_color, who_desc = HealthClassifier.get_who_pm25_category(pm25)
            st.markdown('<div class="m-label">🔬 PM2.5</div>', unsafe_allow_html=True)
            pm25_display = f'{pm25} µg/m³' if pm25 else "N/A"
            st.markdown(f'<div class="m-value" style="color:{who_color}; font-size:32px;">{pm25_display}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="m-sub">{who_cat}</div>', unsafe_allow_html=True)
        
        with m3:
            st.markdown('<div class="m-label">🌡️ Temperature</div>', unsafe_allow_html=True)
            temp = data.get("temp")
            temp_display = f"{temp}°C" if temp else "N/A"
            st.markdown(f'<div class="m-value" style="font-size:32px;">{temp_display}</div>', unsafe_allow_html=True)
        
        with m4:
            st.markdown('<div class="m-label">💧 Humidity</div>', unsafe_allow_html=True)
            humidity = data.get("humidity")
            humidity_display = f"{humidity}%" if humidity else "N/A"
            st.markdown(f'<div class="m-value" style="font-size:32px;">{humidity_display}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # AQI Predictor Section
        st.markdown('<div id="predictor"></div>', unsafe_allow_html=True)
        st.markdown("## 📈 6-Hour AQI Forecast")
        
        if aqi:
            with st.spinner("🔮 Generating forecast..."):
                predictor = AQIPredictor()
                forecast = predictor.predict_6hr_trend(aqi)
                
                # Create forecast visualization
                hours = [f"+{i}h" for i in range(1, 7)]
                all_hours = ["Now"] + hours
                all_values = [aqi] + forecast
                
                fig = go.Figure()
                
                fig.add_trace(go.Scatter(
                    x=all_hours,
                    y=all_values,
                    mode='lines+markers',
                    name='AQI Forecast',
                    line=dict(color='#3b82f6', width=3),
                    marker=dict(size=10, color='#3b82f6')
                ))
                
                # Add color bands
                fig.add_hrect(y0=0, y1=50, fillcolor="#00d26a", opacity=0.1, line_width=0, annotation_text="Good", annotation_position="right")
                fig.add_hrect(y0=50, y1=100, fillcolor="#facc15", opacity=0.1, line_width=0, annotation_text="Moderate", annotation_position="right")
                fig.add_hrect(y0=100, y1=150, fillcolor="#fb923c", opacity=0.1, line_width=0, annotation_text="Unhealthy (SG)", annotation_position="right")
                fig.add_hrect(y0=150, y1=200, fillcolor="#f97316", opacity=0.1, line_width=0, annotation_text="Unhealthy", annotation_position="right")
                fig.add_hrect(y0=200, y1=500, fillcolor="#ef4444", opacity=0.1, line_width=0, annotation_text="Very Unhealthy", annotation_position="right")
                
                fig.update_layout(
                    title="AQI Trend Forecast",
                    xaxis_title="Time",
                    yaxis_title="AQI",
                    template="plotly_dark",
                    height=400,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Forecast summary
                st.markdown("### 📊 Forecast Summary")
                fc1, fc2, fc3 = st.columns(3)
                
                with fc1:
                    trend = "Improving 📉" if forecast[-1] < aqi else "Worsening 📈" if forecast[-1] > aqi else "Stable ➡️"
                    st.metric("Trend", trend)
                
                with fc2:
                    avg_forecast = sum(forecast) / len(forecast)
                    st.metric("Avg Forecast", f"{avg_forecast:.0f}")
                
                with fc3:
                    max_forecast = max(forecast)
                    st.metric("Peak AQI", f"{max_forecast}")
        
        st.markdown("---")
        
        # Other pollutants
        st.markdown("## 🧪 Other Pollutants")
        pcols = st.columns(5)
        pollutants = [
            ("PM10", data.get("pm10"), "🌫️"),
            ("O₃", data.get("o3"), "☁️"),
            ("NO₂", data.get("no2"), "🏭"),
            ("SO₂", data.get("so2"), "⚗️"),
            ("CO", data.get("co"), "💨")
        ]
        
        for idx, (name, value, icon) in enumerate(pollutants):
            with pcols[idx]:
                val_display = f"{value}" if value is not None else "N/A"
                pcols[idx].metric(f"{icon} {name}", val_display)
        
        # Weather conditions
        st.markdown('<div class="weather-container">', unsafe_allow_html=True)
        st.markdown("<p style='color:#00d26a; font-weight:700;'>🌤️ Current Weather Conditions</p>", unsafe_allow_html=True)
        
        w1, w2, w3, w4 = st.columns(4)
        w1.metric("🌡️ Temp", f"{data.get('temp', 'N/A')}°C")
        w2.metric("💧 Humidity", f"{data.get('humidity', 'N/A')}%")
        w3.metric("💨 Wind", f"{data.get('wind', 'N/A')} km/h")
        w4.metric("🎚️ Pressure", f"{data.get('pressure', 'N/A')} hPa")
        st.markdown("</div>", unsafe_allow_html=True)
    
    else:
        st.info("👆 Enter a location above to view detailed air quality dashboard")
