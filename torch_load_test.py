import torch

file_path ="/home/drakosfire/Documents/model/ttrpg-mini-figurinev1/model/ttrpg-mini-figure-000003.safetensors"
try:
    # Attempt to load the model file directly without any additional processing
    state_dict = torch.load(file_path, map_location='cpu')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Failed to load model: {str(e)}")

# Try opening the file as a binary to see the initial characters
with open(file_path, 'rb') as f:
    print(f.read(100))  # Read and print the first 10 bytes
