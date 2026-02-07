"""
Machine learning models for AQI prediction and clustering
"""
import numpy as np
from sklearn.cluster import KMeans
from xgboost import XGBRegressor
from typing import List


class AQIPredictor:
    """Simple AQI forecasting model"""
    
    @staticmethod
    def predict_6hr_trend(current_aqi: int) -> List[int]:
        """
        Generates 6 hourly data points starting from the current AQI.
        
        Args:
            current_aqi: Current AQI value
            
        Returns:
            List of 6 integers representing hourly forecast [+1h, +2h, +3h, +4h, +5h, +6h]
        """
        forecast = []
        last_val = current_aqi
        
        for i in range(1, 7):
            # Random walk variation to simulate air quality changes
            variation = np.random.randint(-5, 6)
            last_val = last_val + variation
            # Keep value within realistic AQI bounds (0-500)
            forecast.append(max(0, min(500, last_val)))
        
        return forecast


class AQIClusterer:
    """K-means clustering for AQI severity analysis"""
    
    @staticmethod
    def cluster_aqis(aqis: List[float], n_clusters: int = 3) -> List[float]:
        """
        Cluster AQI values using K-means
        
        Args:
            aqis: List of AQI values
            n_clusters: Number of clusters (default 3, max = len(aqis))
            
        Returns:
            Sorted list of cluster centers
        """
        k = min(n_clusters, len(aqis))
        model = KMeans(n_clusters=k, n_init=10, random_state=42)
        model.fit(np.array(aqis).reshape(-1, 1))
        return sorted(model.cluster_centers_.flatten())
