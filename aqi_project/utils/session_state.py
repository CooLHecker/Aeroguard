"""
Session state management
"""
import streamlit as st


def initialize_session_state():
    """Initialize all session state variables"""
    
    # View state
    if "view" not in st.session_state:
        st.session_state.view = "home"
    
    # Location search state
    if "location_query" not in st.session_state:
        st.session_state.location_query = ""
    
    if "last_searched_query" not in st.session_state:
        st.session_state.last_searched_query = ""
    
    if "waqi_search_results" not in st.session_state:
        st.session_state.waqi_search_results = []
    
    if "selected_station_uid" not in st.session_state:
        st.session_state.selected_station_uid = None
    
    if "selected_station_label" not in st.session_state:
        st.session_state.selected_station_label = None
    
    # Map view state
    if "map_location" not in st.session_state:
        st.session_state.map_location = None
    
    if "map_stations" not in st.session_state:
        st.session_state.map_stations = None
    
    if "map_centers" not in st.session_state:
        st.session_state.map_centers = None
    
    # Dashboard state
    if "dashboard_location" not in st.session_state:
        st.session_state.dashboard_location = None
    
    if "dashboard_data" not in st.session_state:
        st.session_state.dashboard_data = None
