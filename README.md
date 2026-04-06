# Grade Crossing Visual Distractions - MBS Externship F26

## Project Overview
This project identifies and analyzes potential visual distractions at railroad grade crossings. Using a combination of Google Street View imagery, computer vision, and weighted risk analysis, the system evaluates the density of objects that may obstruct a driver's view or distract them from seeing oncoming trains.

The primary goal is to provide a scalable tool for safety inspectors and urban planners to prioritize grade crossings for physical improvements or further inspection.

## Project Team
**MBS Externship Collabrative Solutions F26 Visual Distractions Team**

## System Architecture
The project follows a three-stage pipeline managed by a central execution script (`main.py`).

### 1. Dataset Generation (`dataset_generation.py`)
- **Function**: Retrieves 360-degree street-level imagery for specific GPS coordinates.
- **Input**: `coordinates.csv` containing latitude (`lat`) and longitude (`lng`) columns.
- **Output**: JPG images saved in the `data/` directory, named with the format `sv_lat_lng.jpg`.
- **Note**: Requires a valid Google Maps Street View Static API key.

### 2. Object Detection (`detector.py`)
- **Function**: Performs object detection on the collected imagery using a custom-trained YOLOv5 model.
- **Target Classes**: Trees, poles, buildings, billboards, and signs.
- **Model**: `model/best.pt` (weights) loaded via the local `yolov5` directory.
- **Output**: `detections.csv`, which logs every detected object, its confidence score, bounding box coordinates, and associated GPS location.

### 3. Risk Analysis (`risk_analyzer.py`)
- **Function**: Calculates a numerical risk score for each location based on the types and quantities of detected objects.
- **Weighting Logic**:
    - Poles: 0.3
    - Trees: 0.2
    - Billboards: 0.2
    - Signs: 0.2
    - Buildings: 0.1
- **Output**: `risk_summary.csv`, a prioritized list of locations sorted by their calculated risk score.

## Installation and Setup

### Prerequisites
- Python 3.8+
- PyTorch (with CUDA support for faster processing)
- Google Maps API Key

### Installation
1. Clone the repository and navigate to the project root.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. (Optional) Ensure the `yolov5` submodule or directory is properly configured.

### Configuration
1. Add your Google Maps API key to the `API_KEY` variable in `dataset_generation.py`.
2. Place your list of target locations in `coordinates.csv` in the root directory.

## Usage
To run the entire pipeline from image collection to final risk report:
```bash
python main.py
```

## Expected Output Example

### risk_summary.csv
The final analysis provides a consolidated view of each location. A higher `risk_score` indicates a higher density of distracting elements.

| lat | lng | tree | pole | building | billboard | sign | risk_score |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 40.7128 | -74.0060 | 4 | 2 | 1 | 1 | 3 | 2.3 |
| 34.0522 | -118.2437 | 2 | 1 | 0 | 0 | 5 | 1.7 |
| 41.8781 | -87.6298 | 1 | 3 | 2 | 0 | 2 | 1.7 |
| 29.7604 | -95.3698 | 0 | 1 | 1 | 1 | 1 | 0.8 |

*Note: The risk score is calculated by multiplying the count of each object class by its assigned weight.*
