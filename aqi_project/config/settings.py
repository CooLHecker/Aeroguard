"""
Configuration settings for AeroGuard application
"""
from zoneinfo import ZoneInfo

# Timezone Configuration
IST = ZoneInfo("Asia/Kolkata")

# WAQI API Configuration
WAQI_TOKEN = "9c765b272d5fb3a2bcad06497823f7ce67c15c8b"

# App Configuration
APP_TITLE = "AeroGuard"
PAGE_LAYOUT = "wide"

# Map Configuration
MAP_DEFAULT_ZOOM = 11
MAP_DELTA = 0.6
MAP_TILES = "CartoDB positron"
HEATMAP_RADIUS = 40
HEATMAP_BLUR = 25
HEATMAP_MAX_ZOOM = 13

# AQI Thresholds
AQI_THRESHOLDS = {
    "good": 50,
    "moderate": 100,
    "unhealthy_sg": 150,
    "unhealthy": 200,
    "very_unhealthy": 300,
    "hazardous": 500
}

# WHO PM2.5 Guidelines
WHO_PM25_THRESHOLDS = {
    "good": 15,
    "fair": 25,
    "moderate": 37.5,
    "poor": 75
}

# Color Scheme
COLORS = {
    "good": "#00d26a",
    "moderate": "#facc15",
    "unhealthy_sg": "#fb923c",
    "unhealthy": "#f97316",
    "very_unhealthy": "#ef4444",
    "hazardous": "#7f1d1d",
    "unknown": "#9ca3af"
}

# Cache TTL (seconds)
CACHE_TTL = 900  # 15 minutes
