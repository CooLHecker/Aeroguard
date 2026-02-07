"""
Main application entry point for AeroGuard
"""
import streamlit as st
from config.settings import APP_TITLE, PAGE_LAYOUT
from utils.session_state import initialize_session_state
from ui.styles import get_global_css
from ui.navbar import render_navbar
from ui.views.home import render_home
from ui.views.dashboard import render_dashboard
from ui.views.heatmap import render_heatmap
from ui.views.scheduler import render_scheduler
from ui.views.health_risk import render_health_risk


def main():
    """Main application function"""
    
    # Page configuration
    st.set_page_config(page_title=APP_TITLE, layout=PAGE_LAYOUT)
    
    # Initialize session state
    initialize_session_state()
    
    # Apply global CSS
    st.markdown(get_global_css(), unsafe_allow_html=True)
    
    # Render navbar
    render_navbar()
    
    # Routing
    action = st.query_params.get("action")
    if action in {"home", "dashboard", "scheduler", "health_risk", "heatmap"}:
        st.session_state.view = action
    
    # Render appropriate view
    if st.session_state.view == "home":
        render_home()
    elif st.session_state.view == "dashboard":
        render_dashboard()
    elif st.session_state.view == "heatmap":
        render_heatmap()
    elif st.session_state.view == "scheduler":
        render_scheduler()
    elif st.session_state.view == "health_risk":
        render_health_risk()


if __name__ == "__main__":
    main()
