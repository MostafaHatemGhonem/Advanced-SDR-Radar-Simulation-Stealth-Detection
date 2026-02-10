import requests
import json
import os

creds_data = {
    "clientId": "omar-mohamed-252-api-client",
    "clientSecret": "pyP1EaFj3Ok5c2OjMZodbDgdx3ReLXmx"
}

with open('credentials.json', 'w') as f:
    json.dump(creds_data, f)

def get_credentials():
    with open('credentials.json', 'r') as f:
        creds = json.load(f)
    return creds['clientId'], creds['clientSecret']

URL = "https://opensky-network.org/api/states/all"

def fetch_raw_data():
    username, password = get_credentials()
    
    # Try with authentication first
    try:
        print("Attempting authenticated access...")
        response = requests.get(URL, auth=(username, password), timeout=15)

        if response.status_code == 200:
            print("[OK] Authentication successful!")
            data = response.json()
            return data.get('states', [])
        elif response.status_code == 401:
            print(f"[WARNING] Authentication failed (401 Unauthorized)")
            print("[INFO] Trying anonymous access...")
            # Fallback to anonymous access
            response = requests.get(URL, timeout=15)
            if response.status_code == 200:
                print("[OK] Anonymous access successful!")
                data = response.json()
                return data.get('states', [])
            else:
                print(f"[ERROR] Anonymous access also failed: Status code {response.status_code}")
                return None
        else:
            print(f"[ERROR] Authentication failed: Status code {response.status_code}")
            return None
    except Exception as e:
        print(f"Exception occurred: {e}")
        return None

if __name__ == "__main__":
    print("Fetching live flight data... Please wait.")
    print(f"[DEBUG] Current working directory: {os.getcwd()}")
    
    flights_data = fetch_raw_data()

    if flights_data:
        print(f"\nFetched data for {len(flights_data)} flights successfully!")
        print("-" * 80)
        
        # Save raw data to JSON with absolute path
        output_file = os.path.join(os.getcwd(), 'all_flights_raw.json')
        print(f"[DEBUG] Saving to: {output_file}")
        
        try:
            with open(output_file, 'w') as f:
                json.dump(flights_data, f, indent=2)
            print(f"[OK] Saved raw data to '{output_file}'")
            
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                print(f"[OK] File exists! Size: {file_size:,} bytes")
            else:
                print("[ERROR] File was not created!")
                
        except Exception as e:
            print(f"[ERROR] Failed to save file: {e}")
        
        print(f"\nSummary: {len(flights_data)} flights from around the world")
        print("\nFirst 8 flights preview:")
        for flight in flights_data[:8]:
            callsign = flight[1].strip() if flight[1] else 'Unknown'
            print(f"  ID: {flight[0]} | Flight: {callsign:10} | Country: {flight[2]:20} | Alt: {flight[7]}m")
    else:
        print("Failed to fetch data. Check your internet connection or API limits.")

        # form omar