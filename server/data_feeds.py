import httpx
import os

# Open-Meteo — free, no API key needed
async def get_weather(lat: float, lon: float) -> str:
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,precipitation,windspeed_10m"
        f"&daily=precipitation_sum,temperature_2m_max,temperature_2m_min"
        f"&timezone=Asia%2FKolkata&forecast_days=3"
    )
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(url)
            r.raise_for_status()
            d = r.json()
            cur = d["current"]
            daily = d["daily"]
            return (
                f"मौसम: तापमान {cur['temperature_2m']}°C, "
                f"हवा {cur['windspeed_10m']} km/h, "
                f"बारिश {cur['precipitation']} mm। "
                f"अगले 3 दिन बारिश: {daily['precipitation_sum']}"
            )
    except Exception as e:
        return ""

# District → lat/lon mapping (top farming districts)
DISTRICT_COORDS = {
    "default": (26.8, 80.9),   # Lucknow UP
    "punjab":  (30.9, 75.8),   # Ludhiana
    "haryana": (29.9, 76.8),   # Karnal
    "mp":      (23.2, 77.4),   # Bhopal
    "maha":    (19.9, 75.3),   # Aurangabad
    "bihar":   (25.6, 85.1),   # Patna
    "rajasthan": (26.9, 75.8), # Jaipur
}

def get_coords_for_phone(phone: str) -> tuple:
    """Rough district guess from phone prefix (91 + STD code)."""
    prefix = phone[2:7] if phone.startswith("91") else phone[:5]
    # STD code → state (very rough)
    if prefix[:4] in ("9417", "9814", "9815", "9876"):
        return DISTRICT_COORDS["punjab"]
    if prefix[:4] in ("9812", "9813", "8059"):
        return DISTRICT_COORDS["haryana"]
    if prefix[:4] in ("9425", "9826", "8989"):
        return DISTRICT_COORDS["mp"]
    if prefix[:4] in ("9823", "9763", "8888"):
        return DISTRICT_COORDS["maha"]
    if prefix[:4] in ("9771", "9973", "8877"):
        return DISTRICT_COORDS["bihar"]
    return DISTRICT_COORDS["default"]

# Agmarknet mock (site blocks scraping; use static fallback)
MANDI_PRICES = {
    "गेहूं": "₹2,275/क्विंटल (MSP)",
    "धान":  "₹2,300/क्विंटल (MSP)",
    "मक्का": "₹2,090/क्विंटल (MSP)",
    "कपास": "₹7,121/क्विंटल (MSP)",
    "सोयाबीन": "₹4,892/क्विंटल (MSP)",
}

def get_mandi_price(query: str) -> str:
    for crop, price in MANDI_PRICES.items():
        if crop in query:
            return f"{crop} का भाव: {price}"
    return ""