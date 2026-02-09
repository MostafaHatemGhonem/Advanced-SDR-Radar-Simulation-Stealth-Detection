import math

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    distance = R * c
    return distance


aircrafts = [
    {"id": "A1", "lat": 30.05, "lon": 31.20, "altitude": 10000},
    {"id": "A2", "lat": 29.00, "lon": 30.00, "altitude": 0},
    {"id": "A3", "lat": 35.00, "lon": 40.00, "altitude": 8000}
]

radar_lat = 30.0444   # in cairo
radar_lon = 31.2357

def filter_aircrafts(aircrafts, radar_lat, radar_lon, max_range=150):
    result = []
    
    for plane in aircrafts:
        distance = haversine(radar_lat, radar_lon, plane["lat"], plane["lon"])
        
        if distance <= max_range and plane["altitude"] > 0:
            plane["distance"] = round(distance, 2)
            result.append(plane)
    
    return result

valid_planes = filter_aircrafts(aircrafts, radar_lat, radar_lon)
print(valid_planes)
