import requests
import os

API_KEY = os.getenv("GOOGLE_PLACES_API_KEY")

def get_nearby_hospitals(lat, lng, radius=5000):
    if not lat or not lng:
        return []

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": "hospital",
        "key": API_KEY
    }

    res = requests.get(url, params=params, timeout=5)
    data = res.json()

    hospitals = []
    for place in data.get("results", [])[:7]:
        hospitals.append({
            "name": place.get("name"),
            "address": place.get("vicinity"),
            "rating": place.get("rating"),
            "map": (
                "https://www.google.com/maps/place/?q=place_id="
                + place.get("place_id")
            )
        })

    return hospitals
