from services.google_places import get_nearby_hospitals
from data.hospitals import DEFAULT_HOSPITALS
from utils.maps import google_maps_link

def resolve_hospitals(disease, lat, lng, fallback_location):
    hospitals = get_nearby_hospitals(lat, lng)

    if hospitals:
        return hospitals

    # fallback if Google Places fails
    return [
        {
            "name": h,
            "map": google_maps_link(h, fallback_location)
        }
        for h in DEFAULT_HOSPITALS.get(disease, [])
    ]
