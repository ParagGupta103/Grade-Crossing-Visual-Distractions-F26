import os
import time
import requests
import pandas as pd
from dotenv import load_dotenv

# Load the API key securely
load_dotenv()
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

if not API_KEY:
    print("❌ Error: API Key not found. Please check your .env file.")
    exit()

# --- CONFIGURATION ---
CSV_FILE = "coordinates.csv"
OUTPUT_DIR = "data"
IMAGE_SIZE = "600x400"
SEARCH_RADIUS = 500  

os.makedirs(OUTPUT_DIR, exist_ok=True)

try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    print(f"❌ Error: Could not find '{CSV_FILE}'.")
    exit()

base_url = "https://maps.googleapis.com/maps/api/streetview"

# We are now taking 8 photos per location (360 / 45 = 8)
total_expected = len(df) * 8
print(f"Starting High-Coverage sweep for {len(df)} locations (Total expected images: {total_expected})...")

for index, row in df.iterrows():
    lat = str(row["lat"]).strip()
    lng = str(row["lng"]).strip()

    # range(0, 360, 45) creates the list: [0, 45, 90, 135, 180, 225, 270, 315]
    for current_heading in range(0, 360, 45):
        
        params = {
            "size": IMAGE_SIZE,
            "location": f"{lat},{lng}",
            "key": API_KEY,
            "fov": 120,  # Maximize the field of view for wider coverage
            "heading": current_heading,  
            "pitch": 0,
            "radius": SEARCH_RADIUS,  
            "return_error_code": "true" 
        }

        filename = os.path.join(OUTPUT_DIR, f"sv_{lat}_{lng}_deg{current_heading}.jpg")
        
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            with open(filename, "wb") as file:
                file.write(response.content)
            print(f"[{index + 1}/{len(df)}] ✅ Saved {lat}, {lng} facing {current_heading}°")
            
        elif response.status_code == 404:
            print(f"[{index + 1}/{len(df)}] ❌ No imagery found at {lat}, {lng} for {current_heading}° (404).")
            
        elif response.status_code == 403:
            print(f"[{index + 1}/{len(df)}] ❌ Permission Denied (403) for {lat}, {lng}.")
            
        else:
            print(f"[{index + 1}/{len(df)}] ❌ Failed. HTTP {response.status_code}")

        time.sleep(0.1)

print("\n🎉 High-Coverage Dataset generation complete!")