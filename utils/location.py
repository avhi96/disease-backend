import requests

def detect_location(ip):
    try:
        res = requests.get(f"https://ipapi.co/{ip}/json/", timeout=3)
        data = res.json()

        return {
            "city": data.get("city"),
            "state": data.get("region"),
            "lat": data.get("latitude"),
            "lng": data.get("longitude")
        }
    except Exception:
        return {
            "city": None,
            "state": None,
            "lat": None,
            "lng": None
        }
