"""
Health classification and risk assessment utilities
"""
from typing import Tuple, List, Optional
from config.settings import COLORS, AQI_THRESHOLDS, WHO_PM25_THRESHOLDS


class HealthClassifier:
    """Classify air quality health risks based on WHO and EPA standards"""
    
    @staticmethod
    def aqi_band(aqi: Optional[int]) -> str:
        """Get AQI category band"""
        if aqi is None:
            return "Unknown"
        if aqi <= AQI_THRESHOLDS["good"]:
            return "Good"
        if aqi <= AQI_THRESHOLDS["moderate"]:
            return "Moderate"
        if aqi <= AQI_THRESHOLDS["unhealthy_sg"]:
            return "Unhealthy for Sensitive Groups"
        if aqi <= AQI_THRESHOLDS["unhealthy"]:
            return "Unhealthy"
        if aqi <= AQI_THRESHOLDS["very_unhealthy"]:
            return "Very Unhealthy"
        return "Hazardous"
    
    @staticmethod
    def get_who_pm25_category(pm25: Optional[float]) -> Tuple[str, str, str]:
        """
        Returns (category, color, description) based on WHO PM2.5 guidelines
        
        Args:
            pm25: PM2.5 concentration in µg/m³
            
        Returns:
            Tuple of (category_name, hex_color, description)
        """
        if pm25 is None:
            return ("Unknown", COLORS["unknown"], "Data unavailable")
        
        if pm25 <= WHO_PM25_THRESHOLDS["good"]:
            return ("Good", COLORS["good"], "Air quality meets WHO interim target-4")
        elif pm25 <= WHO_PM25_THRESHOLDS["fair"]:
            return ("Fair", COLORS["moderate"], "Exceeds WHO interim target-3")
        elif pm25 <= WHO_PM25_THRESHOLDS["moderate"]:
            return ("Moderate", COLORS["unhealthy_sg"], "Exceeds WHO interim target-2")
        elif pm25 <= WHO_PM25_THRESHOLDS["poor"]:
            return ("Poor", COLORS["unhealthy"], "Exceeds WHO interim target-1")
        else:
            return ("Very Poor", COLORS["very_unhealthy"], "Far exceeds all WHO guidelines")
    
    @staticmethod
    def get_epa_category(aqi: Optional[int]) -> Tuple[str, str, str, List[str]]:
        """
        Returns (category, color, health_implications, actions) based on EPA standards
        
        Args:
            aqi: AQI value
            
        Returns:
            Tuple of (category, color, health_description, recommended_actions_list)
        """
        if aqi is None:
            return ("Unknown", COLORS["unknown"], "Data unavailable", [])
        
        if aqi <= 50:
            return (
                "Good",
                COLORS["good"],
                "Air quality is satisfactory, and air pollution poses little or no risk.",
                ["Enjoy outdoor activities", "No health precautions needed"]
            )
        elif aqi <= 100:
            return (
                "Moderate",
                COLORS["moderate"],
                "Air quality is acceptable. However, there may be a risk for some people who are unusually sensitive to air pollution.",
                ["Unusually sensitive people should consider limiting prolonged outdoor exertion"]
            )
        elif aqi <= 150:
            return (
                "Unhealthy for Sensitive Groups",
                COLORS["unhealthy_sg"],
                "Members of sensitive groups may experience health effects. The general public is less likely to be affected.",
                [
                    "Children, elderly, and people with respiratory conditions should limit outdoor activities",
                    "Consider moving activities indoors",
                    "Reduce prolonged or heavy exertion outdoors"
                ]
            )
        elif aqi <= 200:
            return (
                "Unhealthy",
                COLORS["unhealthy"],
                "Some members of the general public may experience health effects; members of sensitive groups may experience more serious health effects.",
                [
                    "Everyone should reduce prolonged outdoor exertion",
                    "Sensitive groups should avoid all outdoor physical activity",
                    "Consider wearing a mask if going outside"
                ]
            )
        elif aqi <= 300:
            return (
                "Very Unhealthy",
                COLORS["very_unhealthy"],
                "Health alert: The risk of health effects is increased for everyone.",
                [
                    "Everyone should avoid prolonged outdoor exertion",
                    "Sensitive groups should remain indoors",
                    "Close windows and use air purifiers",
                    "Wear N95 masks if must go outside"
                ]
            )
        else:
            return (
                "Hazardous",
                COLORS["hazardous"],
                "Health warning of emergency conditions: everyone is more likely to be affected.",
                [
                    "Everyone should avoid all outdoor activities",
                    "Remain indoors with windows closed",
                    "Use air purifiers on high settings",
                    "Seek medical attention if experiencing symptoms"
                ]
            )
    
    @staticmethod
    def advice_for_age_and_aqi(age: int, aqi: Optional[int]) -> Tuple[str, str, List[str], str]:
        """
        Generate personalized advice based on age and AQI
        
        Args:
            age: User's age
            aqi: Current AQI value
            
        Returns:
            Tuple of (band, message, task_list, color_hex)
        """
        band = HealthClassifier.aqi_band(aqi)
        sensitive = age <= 12 or age >= 60
        
        if aqi is None:
            return band, "AQI unavailable. Try again later.", ["Indoor-only (light)"], COLORS["unknown"]
        
        if aqi <= 50:
            return band, "Great time for outdoor activities.", ["Outdoor workout", "Walk / run", "Errands"], COLORS["good"]
        
        if aqi <= 100:
            if sensitive:
                return (
                    band,
                    "OK for most, but kids/seniors should reduce prolonged outdoor exertion.",
                    ["Short outdoor walk", "Indoor workout", "Errands (short)"],
                    COLORS["moderate"],
                )
            return band, "Generally OK. If symptoms appear, reduce intensity.", ["Outdoor workout (moderate)", "Errands"], COLORS["moderate"]
        
        if aqi <= 150:
            if sensitive:
                return (
                    band,
                    "For kids/seniors: avoid outdoor exertion. Prefer indoor activities.",
                    ["Indoor workout", "Indoor chores", "Air purifier time"],
                    COLORS["unhealthy_sg"],
                )
            return band, "Limit prolonged outdoor exertion.", ["Indoor workout", "Short essential errands"], COLORS["unhealthy_sg"]
        
        if aqi <= 200:
            return band, "Avoid outdoor activities; prefer indoors.", ["Indoor workout", "Mask if must go out"], COLORS["unhealthy"]
        
        return band, "Stay indoors; avoid outdoor exposure.", ["Indoor only", "Close windows", "Air purifier time"], COLORS["very_unhealthy"]
