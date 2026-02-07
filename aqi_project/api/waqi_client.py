"""
WAQI API client for fetching air quality data
"""
import requests
from typing import Optional, Tuple, Dict, List, Any
from config.settings import WAQI_TOKEN


class WAQIClient:
    """Client for interacting with WAQI API"""
    
    BASE_URL = "https://api.waqi.info"
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or WAQI_TOKEN
    
    def _has_token(self) -> bool:
        """Check if token is available"""
        return bool(self.token)
    
    def search_places(self, keyword: str) -> Tuple[Optional[List[Dict]], Optional[Dict]]:
        """
        Search for air quality monitoring stations by keyword
        
        Args:
            keyword: Search term (city, place name, etc.)
            
        Returns:
            Tuple of (results_list, error_dict)
        """
        if not self._has_token():
            return None, {"error": "Missing WAQI token."}
        
        keyword = (keyword or "").strip()
        if not keyword:
            return [], None
        
        url = f"{self.BASE_URL}/search/"
        params = {"keyword": keyword, "token": self.token}
        
        try:
            r = requests.get(url, params=params, timeout=12)
            data = r.json()
        except Exception as e:
            return None, {"error": f"Network/parse error: {e}"}
        
        if data.get("status") != "ok":
            return None, data
        
        results = data.get("data", []) or []
        
        # Normalize results
        normalized = []
        for item in results:
            uid = item.get("uid")
            station = item.get("station", {}) or {}
            name = station.get("name") or "Unknown station"
            geo = station.get("geo") or []
            lat = geo[0] if len(geo) >= 1 else None
            lon = geo[1] if len(geo) >= 2 else None
            aqi = item.get("aqi")
            time = item.get("time", {}) or {}
            time_s = time.get("stime") or time.get("s")
            
            normalized.append({
                "uid": uid,
                "name": name,
                "aqi": aqi,
                "time": time_s,
                "lat": lat,
                "lon": lon,
            })
        
        return normalized, None
    
    def get_feed_by_uid(self, uid: int) -> Tuple[Optional[Dict], Optional[Dict]]:
        """
        Get detailed air quality data for a specific station by UID
        
        Args:
            uid: Station unique identifier
            
        Returns:
            Tuple of (data_dict, error_dict)
        """
        if not self._has_token():
            return None, {"error": "Missing WAQI token."}
        
        url = f"{self.BASE_URL}/feed/@{uid}/"
        params = {"token": self.token}
        
        try:
            r = requests.get(url, params=params, timeout=12)
            data = r.json()
        except Exception as e:
            return None, {"error": f"Network/parse error: {e}"}
        
        if data.get("status") != "ok":
            return None, data
        
        d = data.get("data", {}) or {}
        iaqi = d.get("iaqi", {}) or {}
        
        return {
            "aqi": d.get("aqi"),
            "pm25": iaqi.get("pm25", {}).get("v"),
            "pm10": iaqi.get("pm10", {}).get("v"),
            "o3": iaqi.get("o3", {}).get("v"),
            "no2": iaqi.get("no2", {}).get("v"),
            "so2": iaqi.get("so2", {}).get("v"),
            "co": iaqi.get("co", {}).get("v"),
            "temp": iaqi.get("t", {}).get("v"),
            "humidity": iaqi.get("h", {}).get("v"),
            "wind": iaqi.get("w", {}).get("v"),
            "pressure": iaqi.get("p", {}).get("v"),
            "city": (d.get("city", {}) or {}).get("name"),
            "time": (d.get("time", {}) or {}).get("s"),
            "dominentpol": d.get("dominentpol"),
            "uid": uid,
            "raw": d,
        }, None
    
    def get_feed_by_geo(self, lat: float, lon: float) -> Optional[Dict]:
        """
        Get air quality data by geographic coordinates
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary with air quality data or None
        """
        url = f"{self.BASE_URL}/feed/geo:{lat};{lon}/?token={self.token}"
        try:
            response = requests.get(url).json()
            if response['status'] == 'ok':
                d = response['data']
                return {
                    "aqi": d['aqi'],
                    "pm25": d['iaqi'].get('pm25', {}).get('v', 0),
                    "temp": d['iaqi'].get('t', {}).get('v', 22),
                    "humidity": d['iaqi'].get('h', {}).get('v', 50),
                    "wind": d['iaqi'].get('w', {}).get('v', 5),
                    "city": d['city']['name']
                }
        except Exception:
            return None
    
    def get_bounds_data(self, lat: float, lon: float, delta: float = 0.6) -> List[Dict]:
        """
        Fetch WAQI stations in bounding box
        
        Args:
            lat: Center latitude
            lon: Center longitude
            delta: Bounding box size
            
        Returns:
            List of station data
        """
        if not self._has_token():
            return []
        
        url = (
            f"{self.BASE_URL}/map/bounds/"
            f"?latlng={lat-delta},{lon-delta},{lat+delta},{lon+delta}"
            f"&token={self.token}"
        )
        try:
            res = requests.get(url, timeout=10).json()
            if res.get("status") != "ok":
                return []
            return res["data"]
        except:
            return []
