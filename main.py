import requests
import json
import os

dir = input('Full url to gallery:')
dir = dir.split('/')
dir = dir[3] +':'+ dir[4]

url = f"https://www.picdrop.com/api/content/{dir}/files?limit=500"

response = requests.get(url)
data = json.loads(response.text)

os.makedirs(f"downloads {dir}", exist_ok=True)

for item in data['files']:
    name = item['name']
    file_url = item['thumbnails'][0]['url']  # first thumbnail url, since it holds the higher resolution

    filepath = os.path.join(f"downloads {dir}", name)

    img_response = requests.get(file_url, stream=True)
    if img_response.status_code == 200:
        with open(filepath, "wb") as f:
            for chunk in img_response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded {name}")
    else:
        print(f"Failed to download {name}: {img_response.status_code}")
