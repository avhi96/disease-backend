def google_maps_link(place, city):
    query = f"{place} {city} hospital"
    return f"https://www.google.com/maps/search/{query.replace(' ', '+')}"
