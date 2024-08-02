import os
import requests
import time
import gradio as gr
from pathlib import Path

# Load API key from environment variable
API_KEY = os.getenv('TRIPO3D_API_KEY')
if not API_KEY:
    raise EnvironmentError("TRIPO3D_API_KEY not found in environment variables")

BASE_URL = "https://api.tripo3d.ai/v2/openapi"
headers = {
    "Authorization": f"Bearer {API_KEY}"
}

def upload_image(file_path):
    url = f"{BASE_URL}/upload"
    files = {'file': open(file_path, 'rb')}
    
    response = requests.post(url, headers=headers, files=files)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.json()}")
        return None

def create_image_to_model_task(image_token):
    url = f"{BASE_URL}/task"
    payload = {
        "type": "image_to_model",
        "file": {
            "type": "jpg",  # Adjust this based on the actual file type
            "file_token": image_token
        }
    }

    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.json()}")
        return None

def check_task_status(task_id):
    url = f"{BASE_URL}/task/{task_id}"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}, {response.json()}")
        return None

def download_file(url, local_filename):
    with requests.get(url, headers=headers, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    return local_filename

def process_image(file):
    print(file)
    # Step 1: Upload the image
    upload_response = upload_image(file)
    if not upload_response or upload_response.get('code') != 0:
        return "Error uploading image", None

    image_token = upload_response['data']['image_token']

    # Step 2: Create image-to-model task
    task_response = create_image_to_model_task(image_token)
    if not task_response or task_response.get('code') != 0:
        return "Error creating task", None

    task_id = task_response['data']['task_id']

    # Step 3: Check task status
    while True:
        status_response = check_task_status(task_id)
        if status_response and status_response.get('code') == 0:
            status = status_response['data']['status']
            progress = status_response['data']['progress']
            print(f"Task Status: {status}, Progress: {progress}%")
            
            if status == "success":
                output = status_response['data']['output']
                model_url = output['model']  # Assuming 'model' key contains the URL

                # Step 4: Download the .glb file
                local_filename = f"{task_id}.glb"
                download_file(model_url, local_filename)

                return "3D Model Generated Successfully", local_filename
            elif status in ["failed", "cancelled"]:
                return f"Task {status}", None
            else:
                time.sleep(5)  # Wait for 5 seconds before checking again
        else:
            return "Failed to check task status", None

# Gradio Interface
def gradio_interface(file):
    result, model_path = process_image(file)
    if model_path:
        return result, model_path
    else:
        return result, None

demo = gr.Interface(
    fn=gradio_interface, 
    inputs=gr.Image(type="filepath"), 
    outputs=["text", gr.Model3D()]
)

demo.launch()