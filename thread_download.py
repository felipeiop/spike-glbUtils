import os
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

base_url = "https://storage.googleapis.com/glb-content-bucket/MML/MML/{}.mml"

def download_glb(character_id, glb_url, folder_name):
    response = requests.get(glb_url)
    if response.status_code == 200:
        glb_content = response.content
        folder_path = os.path.join(os.getcwd(), str(character_id))
        os.makedirs(folder_path, exist_ok=True)

        glb_filename = os.path.join(folder_path, os.path.basename(glb_url))

        with open(glb_filename, 'wb') as glb_file:
            glb_file.write(glb_content)

        print(f"Downloaded {glb_url} to {folder_name}")

def process_character(character_id):
    url = base_url.format(character_id)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        character_folder_name = str(character_id)

        glb_urls = [tag['src'] for tag in soup.find_all(['m-model', 'm-character'])]

        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            executor.map(lambda glb_url: download_glb(character_id, glb_url, character_folder_name), glb_urls)

def download_characters(start_id, end_id):
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        executor.map(process_character, range(start_id, end_id + 1))

if __name__ == "__main__":
    start_character_id = 0
    end_character_id = 9999

    download_characters(start_character_id, end_character_id)

