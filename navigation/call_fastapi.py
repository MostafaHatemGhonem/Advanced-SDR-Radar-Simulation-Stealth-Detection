Data={
  "status": "success",
  "radar_center": {"lat": 30.0444, "lon": 31.2357},
  "targets": [
    {
      "id": "T01",
      "callsign": "EGY-123",
      "distance_km": 45.5,
      "azimuth_deg": 30.0,
      "altitude_m": 10000,
      "velocity_ms": 250
    },
    {
      "id": "T02",
      "callsign": "GHOST-X",
      "distance_km": 120.2,
      "azimuth_deg": 185.0,
      "altitude_m": 15000,
      "velocity_ms": 600
    }
  ]
}
#كأنها الداتا اللي هتيجي من عمر

def get_data():
    return Data
  
def filtered_targets(Data) :
    filtered=[]


    for t in Data["targets"]:
        if t["altitude_m"] > 0 and t["distance_km"] <= 150:
            filtered.append(t)

    return {"targets": filtered} 

#مثال لكود سها

from fastapi import FastAPI
app=FastAPI() 
@app.get("/radar") 
def radar():
   data=get_data()
   result=filtered_targets(data)
   return result