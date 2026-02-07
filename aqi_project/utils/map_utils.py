"""
Map visualization utilities using Folium
"""
import folium
import numpy as np
from folium.plugins import HeatMap
from typing import List, Tuple
from config.settings import MAP_DEFAULT_ZOOM, MAP_TILES, HEATMAP_RADIUS, HEATMAP_BLUR, HEATMAP_MAX_ZOOM


class MapVisualizer:
    """Create interactive maps and heatmaps for AQI visualization"""
    
    @staticmethod
    def extract_valid_aqi(stations: List[dict]) -> Tuple[List[float], List[float], List[int]]:
        """
        Extract valid AQI data from station list
        
        Args:
            stations: List of station dictionaries from WAQI API
            
        Returns:
            Tuple of (latitudes, longitudes, aqi_values)
        """
        lats, lons, aqis = [], [], []
        for s in stations:
            try:
                aqi = int(s["aqi"])
                if 0 < aqi <= 500:
                    lats.append(s["lat"])
                    lons.append(s["lon"])
                    aqis.append(aqi)
            except:
                continue
        return lats, lons, aqis
    
    @staticmethod
    def build_heatmap(
        center_lat: float,
        center_lon: float,
        lats: List[float],
        lons: List[float],
        aqis: List[int]
    ) -> folium.Map:
        """
        Build a folium heatmap from AQI data
        
        Args:
            center_lat: Center latitude for map
            center_lon: Center longitude for map
            lats: List of station latitudes
            lons: List of station longitudes
            aqis: List of AQI values
            
        Returns:
            Folium Map object with heatmap layer
        """
        # Normalize weights between 0 and 1
        mn, mx = min(aqis), max(aqis)
        weights = [(v - mn) / (mx - mn + 1e-6) for v in aqis]
        
        # Create base map
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=MAP_DEFAULT_ZOOM,
            tiles=MAP_TILES
        )
        
        # Add heatmap layer
        HeatMap(
            list(zip(lats, lons, weights)),
            radius=HEATMAP_RADIUS,
            blur=HEATMAP_BLUR,
            max_zoom=HEATMAP_MAX_ZOOM
        ).add_to(m)
        
        return m
