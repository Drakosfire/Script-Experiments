import requests
from bs4 import BeautifulSoup  # BeautifulSoup is used for HTML parsing

def index_image_paths(github_path):
    base_url = f"https://github.com/Drakosfire/CardGenerator/tree/main/seed_images/{github_path}"
    raw_base_url = f"https://raw.githubusercontent.com/Drakosfire/CardGenerator/main/seed_images/{github_path}"
    print(f"Raw URL = {base_url}")
    
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)
    
    list_temp_files = []
    # Assuming that the image files are linked in 'a' tags; this might need adjustment
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and github_path in href:
            file_name = href.split('/')[-1]
            image_url = f"{raw_base_url}/{file_name}"
            list_temp_files.append(image_url)
    
    return list_temp_files
print(index_image_paths("item_seeds"))