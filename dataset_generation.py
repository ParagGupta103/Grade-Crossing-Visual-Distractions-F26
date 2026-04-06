import os
import pandas as pd
import requests
import time

# --- Configuration ---
API_KEY = "YOUR_GOOGLE_MAPS_API_KEY"  # Replace with your actual key
CSV_FILE = "coordinates.csv"  # Path to your CSV file
OUTPUT_DIR = "data"  # Folder to save the images
IMAGE_SIZE = "600x400"  # Max free tier size is 640x640

# Create the output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Load coordinates
# Assumes your CSV has columns named 'lat' and 'lng'
try:
    df = pd.read_csv(CSV_FILE)
except FileNotFoundError:
    print(f"Error: Could not find {CSV_FILE}. Please check the path.")
    exit()

base_url = "https://maps.googleapis.com/maps/api/streetview"

print(f"Starting download of {len(df)} images...")

for index, row in df.iterrows():
    lat = row["lat"]
    lng = row["lng"]

    # Define the API parameters
    params = {
        "size": IMAGE_SIZE,
        "location": f"{lat},{lng}",
        "key": API_KEY,
        "fov": 90,  # Field of view (default is 90, max is 120)
        "heading": 0,  # Compass heading (0=North, 90=East, 180=South, 270=West)
        "pitch": 0,  # Camera angle (0=Default, 90=Straight up, -90=Straight down)
    }

    # Construct a unique filename
    filename = os.path.join(OUTPUT_DIR, f"sv_{lat}_{lng}.jpg")

    # Make the HTTP GET request
    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        # Check if the API returned an actual image or a blank "no imagery" thumbnail
        # Google returns a specific small image when no data is available,
        # but 200 OK is still the status code.
        with open(filename, "wb") as file:
            file.write(response.content)
        print(f"[{index + 1}/{len(df)}] Saved image for {lat}, {lng}")
    else:
        print(
            f"[{index + 1}/{len(df)}] Failed to get image for {lat}, {lng}. HTTP Status: {response.status_code}"
        )

    # Optional: Add a small delay to avoid hitting rate limits too aggressively
    time.sleep(0.1)

print("Dataset generation complete!")
