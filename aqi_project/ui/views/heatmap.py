"""
Heatmap view page
"""
import streamlit as st
import numpy as np
from streamlit_folium import st_folium
from api.waqi_client import WAQIClient
from utils.map_utils import MapVisualizer
from models.predictor import AQIClusterer
from config.settings import COLORS


def render_heatmap():
    """Render the heatmap page"""
    
    st.markdown("""
<div class="hero">
    <h1>🗺️ AeroGuard AQI Heatmap</h1>
    <p>AI-driven air quality insights using real WAQI stations</p>
</div>
""", unsafe_allow_html=True)
    
    # Navigation buttons
    col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 4])
    with col_nav1:
        if st.button("🏠 Home", use_container_width=True):
            st.query_params.update({"action": "home"})
            st.session_state.view = "home"
            st.rerun()
    with col_nav2:
        if st.button("📊 Dashboard", use_container_width=True):
            st.query_params.update({"action": "dashboard"})
            st.session_state.view = "dashboard"
            st.rerun()
    
    st.markdown("---")
    
    # Initialize clients
    client = WAQIClient()
    visualizer = MapVisualizer()
    clusterer = AQIClusterer()
    
    # Location input
    st.markdown("## 📍 Location")
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        lat = st.number_input("Latitude", value=19.0760, format="%.6f", help="Enter latitude coordinate")
    
    with col2:
        lon = st.number_input("Longitude", value=72.8777, format="%.6f", help="Enter longitude coordinate")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Generate heatmap button
    if st.button("🗺️ Generate AQI Heatmap", type="primary", use_container_width=True):
        with st.spinner("🔍 Fetching WAQI data and generating heatmap..."):
            stations = client.get_bounds_data(lat, lon)
            lats, lons, aqis = visualizer.extract_valid_aqi(stations)
            
            if len(aqis) < 3:
                st.error("❌ Not enough valid AQI stations found in this area. Try a different location.")
            else:
                st.session_state.map_stations = (lats, lons, aqis)
                st.session_state.map_centers = clusterer.cluster_aqis(aqis)
                st.success(f"✅ Found {len(aqis)} valid AQI monitoring stations")
    
    # Display map
    if st.session_state.map_stations:
        lats, lons, aqis = st.session_state.map_stations
        
        st.markdown("---")
        st.markdown("## 🗺️ Interactive AQI Heatmap")
        
        m = visualizer.build_heatmap(lat, lon, lats, lons, aqis)
        
        st.markdown('<div class="map-wrap">', unsafe_allow_html=True)
        st_folium(m, width=900, height=550)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Display statistics
        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
        with col_stat1:
            st.metric("📡 Stations", len(aqis))
        with col_stat2:
            st.metric("📈 Max AQI", f"{max(aqis):.0f}")
        with col_stat3:
            st.metric("📉 Min AQI", f"{min(aqis):.0f}")
        with col_stat4:
            st.metric("📊 Avg AQI", f"{np.mean(aqis):.1f}")
    
    # AI-learned clusters
    if st.session_state.map_centers:
        st.markdown("---")
        st.markdown("## 🤖 AI-Learned AQI Severity Clusters")
        st.caption("K-means clustering analysis of regional air quality")
        
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        
        for i, c in enumerate(st.session_state.map_centers, 1):
            if c <= 50:
                label = "Good"
                color = COLORS["good"]
            elif c <= 100:
                label = "Moderate"
                color = COLORS["moderate"]
            elif c <= 150:
                label = "Unhealthy (Sensitive Groups)"
                color = COLORS["unhealthy_sg"]
            elif c <= 200:
                label = "Unhealthy"
                color = COLORS["unhealthy"]
            else:
                label = "Very Unhealthy"
                color = COLORS["very_unhealthy"]
            
            st.markdown(
                f"""
<div style="background: #0a0a0a; border-left: 4px solid {color}; padding: 16px; margin: 12px 0; border-radius: 8px;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <div style="color: #9ca3af; font-size: 12px; font-weight: 800;">CLUSTER {i}</div>
            <div style="color: {color}; font-size: 24px; font-weight: 900; margin: 4px 0;">{c:.1f} AQI</div>
        </div>
        <div style="color: {color}; font-size: 18px; font-weight: 700;">{label}</div>
    </div>
</div>
""",
                unsafe_allow_html=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div style="height:100px;"></div>', unsafe_allow_html=True)
