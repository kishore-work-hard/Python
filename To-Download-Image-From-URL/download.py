import os
import requests
from tqdm import tqdm

# Create the folder to save images
if not os.path.exists('images'):
    os.makedirs('images')

# Read the list of URLs from the file
with open('imageurl.txt', 'r') as f:
    urls = f.readlines()

# Download each image and save it in the images folder
for i, url in enumerate(tqdm(urls)):
    try:
        response = requests.get(url.strip(), stream=True)
        response.raise_for_status()
        with open(f'images/image_{i}.jpg', 'wb') as f:
            for chunk in tqdm(response.iter_content(chunk_size=8192), leave=False):
                if chunk:
                    f.write(chunk)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image {i}: {e}")
