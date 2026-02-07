"""
Scheduler view page
"""
import streamlit as st
import datetime
from api.waqi_client import WAQIClient
from utils.health_classifier import HealthClassifier
from config.settings import IST


def render_scheduler():
    """Render the scheduler page"""
    
    st.title("📅 Personalized Scheduler (IST)")
    st.caption("Type a place name → press Enter or click Search → select from dropdown")
    
    now_ist = datetime.datetime.now(tz=IST)
    st.markdown(f"**Current Time (IST):** {now_ist.strftime('%Y-%m-%d %I:%M %p')}")
    
    # Navigation
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
    
    # Initialize client
    client = WAQIClient()
    classifier = HealthClassifier()
    
    # Inputs: Age + Place Search
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 3])
    with c1:
        age = st.number_input("Age", min_value=1, max_value=120, value=25, step=1)
    
    with c2:
        with st.form(key="search_form", clear_on_submit=False):
            search_query = st.text_input(
                "Enter a place name (city / area / station name)",
                value=st.session_state.location_query,
                placeholder="e.g., Delhi, Bandra, Koramangala, Hyderabad",
                help="Press Enter or click Search to load suggestions"
            )
            
            search_button = st.form_submit_button("🔍 Search Locations", use_container_width=True)
        
        if search_button and search_query.strip():
            if search_query != st.session_state.last_searched_query:
                st.session_state.location_query = search_query
                st.session_state.last_searched_query = search_query
                
                with st.spinner("🔍 Searching WAQI stations..."):
                    results, err = client.search_places(search_query)
                
                if err:
                    st.error(f"❌ WAQI search error: {err}")
                    st.session_state.waqi_search_results = []
                else:
                    st.session_state.waqi_search_results = results or []
                    if st.session_state.waqi_search_results:
                        first = st.session_state.waqi_search_results[0]
                        st.session_state.selected_station_uid = first["uid"]
                        st.session_state.selected_station_label = first["name"]
                        st.success(f"✅ Found {len(st.session_state.waqi_search_results)} locations")
                    else:
                        st.warning("⚠️ No locations found. Try a different search term.")
                        st.session_state.selected_station_uid = None
                        st.session_state.selected_station_label = None
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Show dropdown if we have results
    if st.session_state.waqi_search_results:
        st.markdown('<div class="panel">', unsafe_allow_html=True)
        st.markdown("#### 📍 Select Your Location")
        
        options = []
        uid_by_label = {}
        
        for item in st.session_state.waqi_search_results[:25]:
            uid = item["uid"]
            name = item["name"]
            aqi = item.get("aqi")
            lat = item.get("lat")
            lon = item.get("lon")
            
            aqi_txt = f"AQI {aqi}" if aqi not in (None, "-", "") else "AQI ❓"
            
            if isinstance(lat, (int, float)) and isinstance(lon, (int, float)):
                geo_txt = f"📍 {lat:.4f}, {lon:.4f}"
            else:
                geo_txt = "📍 Location data unavailable"
            
            label = f"{name}  |  {aqi_txt}  |  {geo_txt}"
            options.append(label)
            uid_by_label[label] = (uid, name)
        
        chosen_label = st.selectbox(
            "Choose a monitoring station",
            options=options,
            key="location_selector"
        )
        
        if chosen_label:
            st.session_state.selected_station_uid, st.session_state.selected_station_label = uid_by_label.get(chosen_label, (None, None))
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Schedule activity inputs
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("#### 📅 Schedule Your Activity")
    
    d1, d2, d3 = st.columns([1, 1, 1])
    with d1:
        date = st.date_input("Date (IST)", value=datetime.date.today())
    with d2:
        start_time = st.time_input("Start time (IST)", value=datetime.time(7, 0))
    with d3:
        duration_min = st.selectbox("Duration (minutes)", [15, 30, 45, 60, 90, 120], index=1)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Get recommendations button
    if st.button("✨ Get Personalized Recommendations", type="primary", use_container_width=True):
        if not st.session_state.selected_station_uid:
            st.error("❌ Please search and select a location first.")
        else:
            with st.spinner("🔮 Analyzing air quality and generating recommendations..."):
                aqi_data, err = client.get_feed_by_uid(st.session_state.selected_station_uid)
            
            if err:
                st.error(f"❌ Error fetching AQI feed: {err}")
            else:
                aqi = aqi_data.get("aqi")
                city = aqi_data.get("city") or st.session_state.selected_station_label
                pm25 = aqi_data.get("pm25")
                
                st.markdown("---")
                st.markdown(f"### 📊 Results for {city}")
                st.caption(f"Scheduled time: {date} at {start_time.strftime('%I:%M %p')} IST | Duration: {duration_min} minutes")
                
                # Get personalized advice
                band, message, tasks, color = classifier.advice_for_age_and_aqi(age, aqi)
                
                # Display current AQI and health status
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(
                        f"""
<div style="background:#0a0a0a; border-left:4px solid {color}; padding:20px; border-radius:8px;">
    <div style="color:#9ca3af; font-size:12px; font-weight:800;">CURRENT AQI</div>
    <div style="font-size:48px; font-weight:900; color:{color}; margin:12px 0;">{aqi if aqi else "N/A"}</div>
    <div style="color:{color}; font-weight:700; font-size:18px;">{band}</div>
</div>
""",
                        unsafe_allow_html=True
                    )
                
                with col2:
                    who_cat, who_color, who_desc = classifier.get_who_pm25_category(pm25)
                    st.markdown(
                        f"""
<div style="background:#0a0a0a; border-left:4px solid {who_color}; padding:20px; border-radius:8px;">
    <div style="color:#9ca3af; font-size:12px; font-weight:800;">PM2.5 LEVEL</div>
    <div style="font-size:48px; font-weight:900; color:{who_color}; margin:12px 0;">{pm25 if pm25 else "N/A"}</div>
    <div style="color:{who_color}; font-weight:700; font-size:18px;">{who_cat}</div>
</div>
""",
                        unsafe_allow_html=True
                    )
                
                # Personalized message
                st.markdown("### 💡 Personalized Advice")
                st.markdown(
                    f"""
<div style="background:#070707; border:1px solid #1a1a1a; padding:20px; border-radius:12px; margin:16px 0;">
    <p style="color:#e5e7eb; font-size:16px; line-height:1.7;">{message}</p>
</div>
""",
                    unsafe_allow_html=True
                )
                
                # Recommended activities
                st.markdown("### ✅ Recommended Activities")
                for task in tasks:
                    st.markdown(f"- {task}")
                
                st.markdown("---")
                
                # Additional environmental data
                st.markdown("### 🌤️ Environmental Conditions")
                env_cols = st.columns(4)
                
                with env_cols[0]:
                    temp = aqi_data.get("temp")
                    st.metric("🌡️ Temperature", f"{temp}°C" if temp else "N/A")
                
                with env_cols[1]:
                    humidity = aqi_data.get("humidity")
                    st.metric("💧 Humidity", f"{humidity}%" if humidity else "N/A")
                
                with env_cols[2]:
                    wind = aqi_data.get("wind")
                    st.metric("💨 Wind Speed", f"{wind} km/h" if wind else "N/A")
                
                with env_cols[3]:
                    pressure = aqi_data.get("pressure")
                    st.metric("🎚️ Pressure", f"{pressure} hPa" if pressure else "N/A")
    
    st.markdown('<div style="height:100px;"></div>', unsafe_allow_html=True)
