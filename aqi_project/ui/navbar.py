"""
Navigation bar component
"""
import streamlit as st


def render_navbar():
    """Render the sticky navigation bar"""
    st.markdown(
        """
<div class="nav-bar">
    <a href="/?action=home" target="_self" style="text-decoration:none; display:flex; align-items:center; gap:12px;">
        <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="#3b82f6" stroke-width="2">
            <path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"></path>
        </svg>
        <span class="logo-text">AeroGuard</span>
        <span class="badge">🇮🇳 IST • 🔴 Live AQI • 🏥 Health Risk</span>
    </a>
    <div class="nav-links">
        <a href="/?action=home#features" target="_self">Features</a>
        <a href="/?action=home#learn-more" target="_self">Learn More</a>
        <a href="/?action=dashboard" target="_self">Dashboard</a>
        <a href="/?action=heatmap" target="_self">Heatmap</a>
    </div>
    <div class="auth-group">
        <a href="/?action=dashboard" target="_self" class="google-btn" style="background-color:#00d26a;color:#000!important;">
            🚀 Launch Dashboard
        </a>
    </div>
</div>
<div class="header-spacer"></div>
""",
        unsafe_allow_html=True,
    )
