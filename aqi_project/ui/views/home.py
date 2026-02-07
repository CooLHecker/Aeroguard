"""
Home view page
"""
import streamlit as st


def render_home():
    """Render the home page"""
    
    # Hero section
    st.markdown(
        """
<div class="hero-container">
    <h1 class="hero-title">Hyper-Local Air Quality<br>& Health Risk Forecaster</h1>
    <p class="hero-subtitle">
        Move beyond generic AQI numbers. Get personalized, scientifically grounded health risk alerts
        based on who you are and where you are.
    </p>
    <a href="/?action=dashboard" target="_self" class="launch-btn">Launch Dashboard &rarr;</a>
</div>
""",
        unsafe_allow_html=True,
    )
    
    # Features section
    st.markdown('<div id="features" style="height:60px;"></div>', unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; font-size: 42px;'>Core Intelligence</h2>", unsafe_allow_html=True)
    
    st.markdown(
        """
<div class="features-grid">
    <a href="/?action=dashboard#predictor" target="_self" style="text-decoration: none; color: inherit;">
        <div class="feature-card">
            <div class="icon-box">📈</div>
            <h3>AQI Predictor</h3>
            <p>Forecast air quality (AQI / PM2.5) for the next 6 hours using historical time-series data with advanced ML models.</p>
        </div>
    </a>
    <a href="/?action=health_risk" target="_self" style="text-decoration: none; color: inherit;">
        <div class="feature-card">
            <div class="icon-box">🏥</div>
            <h3>Health Risk Classification</h3>
            <p>Convert forecasted AQI into risk levels aligned with WHO and EPA standards, with actionable health advice.</p>
        </div>
    </a>
    <a href="/?action=scheduler" target="_self" style="text-decoration: none; color: inherit;">
        <div class="feature-card">
            <div class="icon-box">📅</div>
            <h3>Personalized Scheduler</h3>
            <p>Type a place name, pick from WAQI suggestions, and get safe task recommendations (IST).</p>
        </div>
    </a>
    <a href="/?action=heatmap" target="_self" style="text-decoration: none; color: inherit;">
        <div class="feature-card">
            <div class="icon-box">🗺️</div>
            <h3>Station-Based Precision</h3>
            <p>Uses WAQI station results for consistent real-time AQI reads with interactive heatmap visualization.</p>
        </div>
    </a>
</div>
""",
        unsafe_allow_html=True,
    )
    
    # Learn more section
    st.markdown('<div id="learn-more" style="height:80px;"></div>', unsafe_allow_html=True)
    st.markdown(
        """
<div class="learn-more-container">
    <h2 style="text-align: center; font-size: 42px;">Why is AQI so high?</h2>
    <p style="text-align: center; color: #666; margin-bottom: 20px;">Understanding the invisible factors that degrade our air.</p>
    <div class="reason-grid">
        <div class="reason-card">
            <h4>Particulate Matter (PM2.5)</h4>
            <p>Tiny particles from combustion and industry that can bypass the body's natural filters.</p>
        </div>
        <div class="reason-card">
            <h4>Thermal Inversions</h4>
            <p>Warm air traps pollutants near the ground like a lid on a pot.</p>
        </div>
        <div class="reason-card">
            <h4>Stagnant Wind Patterns</h4>
            <p>Low air movement prevents dispersion of emissions.</p>
        </div>
        <div class="reason-card">
            <h4>Ground-Level Ozone</h4>
            <p>Sunlight + vehicle exhaust can create a breathable smog.</p>
        </div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )
    
    st.markdown('<div style="height:200px;"></div>', unsafe_allow_html=True)
