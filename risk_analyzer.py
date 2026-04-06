import pandas as pd
import os

# === CONFIGURATION ===
DETECTIONS_CSV = 'detections.csv'
OUTPUT_CSV = 'risk_summary.csv'

# Weights from project
CLASS_WEIGHTS = {
    'tree': 0.2,
    'pole': 0.3,
    'building': 0.1,
    'billboard': 0.2,
    'sign': 0.2
}

def analyze_risk():
    if not os.path.exists(DETECTIONS_CSV):
        print(f"Error: {DETECTIONS_CSV} not found. Please run detector.py first.")
        return

    # 1. Load the detections CSV
    df = pd.read_csv(DETECTIONS_CSV)
    
    if df.empty:
        print("No detections found in the file. Please add images and run detector.py.")
        return

    # 2. Count occurrences of each class PER COORDINATE
    # This automatically groups multiple images for the same location
    counts = df.groupby(['lat', 'lng', 'class']).size().unstack(fill_value=0)
    
    # Ensure all classes from weights are present in columns
    for cls in CLASS_WEIGHTS.keys():
        if cls not in counts.columns:
            counts[cls] = 0
            
    # 3. Calculate Risk Score
    def calculate_score(row):
        score = 0
        for cls, weight in CLASS_WEIGHTS.items():
            score += row.get(cls, 0) * weight
        return round(score, 3)

    counts['risk_score'] = counts.apply(calculate_score, axis=1)
    
    # Sort by risk score descending
    counts = counts.sort_values(by='risk_score', ascending=False)
    
    # 4. Save to final Risk CSV
    counts = counts.reset_index()
    counts.to_csv(OUTPUT_CSV, index=False)
    
    print(f"Risk analysis complete! Results saved to {OUTPUT_CSV}")
    print("\n--- Summary (Top 5 Riskiest Locations) ---")
    print(counts[['lat', 'lng', 'risk_score']].head(5))

if __name__ == "__main__":
    analyze_risk()
