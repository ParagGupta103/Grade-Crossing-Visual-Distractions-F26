import torch
device = 'cpu'
try:
    model = torch.hub.load('yolov5', 'custom', path='model/best.pt', source='local', device=device)
    print("Successfully loaded model from local yolov5")
except Exception as e:
    print(f"Error: {e}")
