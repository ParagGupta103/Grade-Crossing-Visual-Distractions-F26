import os
import pandas as pd
import torch
from pathlib import Path

# === CONFIGURATION ===
MODEL_PATH = 'model/best.pt'
DATA_DIR = 'data'
OUTPUT_CSV = 'detections.csv'
IMG_SIZE = 640
CONF_THRESH = 0.25

def run_detection():
    # 1. Load the Model
    print(f"Loading YOLOv5 model from {MODEL_PATH}...")
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = torch.hub.load('yolov5', 'custom', path=MODEL_PATH, source='local', device=device)
    model.conf = CONF_THRESH
    
    # 2. Process Images
    image_files = list(Path(DATA_DIR).glob('*.jpg')) + list(Path(DATA_DIR).glob('*.png')) + list(Path(DATA_DIR).glob('*.jpeg'))
    
    if not image_files:
        print(f"No images found in {DATA_DIR}. Please add some images first.")
        return

    all_detections = []
    print(f"Processing {len(image_files)} images...")
    
    for img_path in image_files:
        print(f"Scanning {img_path.name}...")
        
        # Parse lat/lng from filename: sv_lat_lng.jpg
        try:
            parts = img_path.stem.split('_')
            lat = float(parts[1])
            lng = float(parts[2])
        except (IndexError, ValueError):
            print(f"  - Warning: Could not parse coordinates from {img_path.name}. Using 0.0, 0.0")
            lat, lng = 0.0, 0.0

        # Run inference
        results = model(str(img_path), size=IMG_SIZE)
        
        # Get detections as a Pandas DataFrame
        detections = results.pandas().xyxy[0] 
        
        # Collect results
        for _, row in detections.iterrows():
            all_detections.append({
                'image_name': img_path.name,
                'lat': lat,
                'lng': lng,
                'class': row['name'],
                'confidence': round(float(row['confidence']), 4),
                'xmin': round(float(row['xmin']), 2),
                'ymin': round(float(row['ymin']), 2),
                'xmax': round(float(row['xmax']), 2),
                'ymax': round(float(row['ymax']), 2)
            })
        
        print(f"  - Found {len(detections)} objects at ({lat}, {lng}).")

    # 3. Save all detections to a CSV file
    if all_detections:
        df = pd.DataFrame(all_detections)
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"\nDetection complete! Results saved to {OUTPUT_CSV}")
    else:
        print("\nNo objects detected in any of the images.")

if __name__ == "__main__":
    run_detection()
