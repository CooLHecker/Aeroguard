"""
Health risk classification view page
"""
import streamlit as st
from api.waqi_client import WAQIClient
from utils.health_classifier import HealthClassifier


def render_health_risk():
    """Render the health risk classification page"""
    
    st.title("🏥 Health Risk Classification")
    st.caption("Understanding air quality standards and health implications from WHO & EPA")
    
    # Navigation
    col_nav1, col_nav2, col_nav3 = st.columns([1, 1, 4])
    with col_nav1:
        if st.button("🏠 Home", use_container_width=True):
            st.query_params.update({"action": "home"})
            st.session_state.view = "home"
            st.rerun()
    with col_nav2:
        if st.button("📅 Try Scheduler", use_container_width=True):
            st.query_params.update({"action": "scheduler"})
            st.session_state.view = "scheduler"
            st.rerun()
    
    st.markdown("---")
    
    # Initialize
    client = WAQIClient()
    classifier = HealthClassifier()
    
    # WHO Guidelines Introduction
    st.markdown("## 🌍 About WHO Air Quality Guidelines")
    st.markdown(
        """
<div class="standard-section">
    <p style="color:#e5e7eb; line-height:1.8; font-size:16px;">
        The <strong>World Health Organization (WHO)</strong> provides evidence-based air quality guidelines to protect public health worldwide. 
        These guidelines are developed through systematic review of scientific evidence on health effects of air pollution and are regularly 
        updated to reflect the latest research findings.
    </p>
    <p style="color:#e5e7eb; line-height:1.8; font-size:16px; margin-top:16px;">
        WHO guidelines focus on <strong>particulate matter (PM2.5 and PM10)</strong>, <strong>ozone (O₃)</strong>, <strong>nitrogen dioxide (NO₂)</strong>, 
        and <strong>sulfur dioxide (SO₂)</strong>. The guidelines recommend interim targets to help countries progressively reduce air pollution 
        and protect their populations, especially vulnerable groups like children, elderly, and those with pre-existing health conditions.
    </p>
    <p style="color:#e5e7eb; line-height:1.8; font-size:16px; margin-top:16px;">
        <strong>PM2.5</strong> (fine particulate matter smaller than 2.5 micrometers) is considered the most harmful pollutant. 
        WHO recommends annual average concentrations should not exceed <strong>5 µg/m³</strong> and 24-hour average should not exceed <strong>15 µg/m³</strong>.
        Countries are encouraged to work toward these guideline values through interim targets (IT-1 through IT-4).
    </p>
</div>
""",
        unsafe_allow_html=True
    )
    
    st.markdown("---")
    
    # Search location for real-time classification
    st.markdown("## 🔍 Check Current Health Risk")
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    
    with st.form(key="health_search_form"):
        search_query = st.text_input(
            "Enter location to check current health risk",
            placeholder="e.g., Delhi, Mumbai, Bangalore",
            help="Press Enter to search"
        )
        search_btn = st.form_submit_button("🔍 Get Health Risk Assessment", use_container_width=True)
    
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
                aqi = aqi_data.get("aqi")
                pm25 = aqi_data.get("pm25")
                
                st.markdown("---")
                st.markdown(f"### 📍 {aqi_data.get('city') or first['name']}")
                
                # Get WHO and EPA classifications
                who_cat, who_color, who_desc = classifier.get_who_pm25_category(pm25)
                epa_cat, epa_color, epa_desc, epa_actions = classifier.get_epa_category(aqi)
                
                # Display current readings
                st.markdown(
                    f"""
<div class="risk-card">
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
        <div style="border-left: 4px solid {who_color}; padding-left: 16px;">
            <div style="color:#9ca3af; font-size:12px; font-weight:800; margin-bottom:8px;">WHO PM2.5 LEVEL</div>
            <div style="font-size:42px; font-weight:900; color:{who_color}; margin:12px 0;">{pm25 if pm25 else "N/A"} <span style="font-size:18px;">µg/m³</span></div>
            <div style="color:{who_color}; font-weight:700; font-size:16px;">{who_cat}</div>
            <div style="color:#9ca3af; font-size:13px; margin-top:8px;">{who_desc}</div>
        </div>
        <div style="border-left: 4px solid {epa_color}; padding-left: 16px;">
            <div style="color:#9ca3af; font-size:12px; font-weight:800; margin-bottom:8px;">EPA AQI</div>
            <div style="font-size:42px; font-weight:900; color:{epa_color}; margin:12px 0;">{aqi if aqi else "N/A"}</div>
            <div style="color:{epa_color}; font-weight:700; font-size:16px;">{epa_cat}</div>
            <div style="color:#9ca3af; font-size:13px; margin-top:8px;">Last updated: {aqi_data.get("time") or "N/A"}</div>
        </div>
    </div>
</div>
""",
                    unsafe_allow_html=True
                )
                
                # Health implications
                st.markdown("### 💊 Health Implications & Recommendations")
                st.markdown(
                    f"""
<div class="standard-section">
    <p style="color:#e5e7eb; font-size:15px; line-height:1.7;">{epa_desc}</p>
    <h4 style="color:#3b82f6; margin-top:20px; margin-bottom:12px;">Recommended Actions:</h4>
    <ul style="color:#9ca3af; line-height:1.8;">
        {''.join([f"<li>{action}</li>" for action in epa_actions])}
    </ul>
</div>
""",
                    unsafe_allow_html=True
                )
                
                # Pollutants breakdown
                st.markdown("### 🧪 Other Pollutants")
                pcols = st.columns(5)
                pollutants = [
                    ("PM10", aqi_data.get("pm10"), "🌫️"),
                    ("O₃", aqi_data.get("o3"), "☁️"),
                    ("NO₂", aqi_data.get("no2"), "🏭"),
                    ("SO₂", aqi_data.get("so2"), "⚗️"),
                    ("CO", aqi_data.get("co"), "💨")
                ]
                
                for idx, (name, value, icon) in enumerate(pollutants):
                    with pcols[idx]:
                        val_display = f"{value}" if value is not None else "N/A"
                        pcols[idx].metric(f"{icon} {name}", val_display)
    
    st.markdown("---")
    
    # Sensitive Groups
    st.markdown("## 👥 Who Are Sensitive Groups?")
    st.markdown(
        """
<div class="standard-section">
    <div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:16px;">
        <div style="background:#0a0a0a; padding:20px; border-radius:8px;">
            <h4 style="color:#3b82f6;">👶 Children</h4>
            <p style="color:#9ca3af; font-size:14px; line-height:1.6;">
                Children's respiratory systems are still developing, and they breathe more air per pound of body weight than adults.
            </p>
        </div>
        <div style="background:#0a0a0a; padding:20px; border-radius:8px;">
            <h4 style="color:#3b82f6;">👴 Older Adults</h4>
            <p style="color:#9ca3af; font-size:14px; line-height:1.6;">
                Seniors may have undiagnosed heart or lung disease, making them more vulnerable to air pollution effects.
            </p>
        </div>
        <div style="background:#0a0a0a; padding:20px; border-radius:8px;">
            <h4 style="color:#3b82f6;">🫁 Respiratory Conditions</h4>
            <p style="color:#9ca3af; font-size:14px; line-height:1.6;">
                People with asthma, COPD, or other lung diseases are particularly sensitive to air pollution.
            </p>
        </div>
        <div style="background:#0a0a0a; padding:20px; border-radius:8px;">
            <h4 style="color:#3b82f6;">❤️ Heart Disease</h4>
            <p style="color:#9ca3af; font-size:14px; line-height:1.6;">
                Cardiovascular disease patients face increased risk from particulate matter exposure.
            </p>
        </div>
    </div>
</div>
""",
        unsafe_allow_html=True
    )
