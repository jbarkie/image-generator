
from base64 import b64decode
import json
from pathlib import Path

def write_image_data_json(response):
    path = Path.cwd() / "responses" / f"{response.created}.json"
    path.parent.mkdir(exist_ok=True)
    with open(path, mode="w", encoding="utf-8") as file:
        json.dump(response.to_dict(), file)

def save_image(response):
    for index, image_dict in enumerate(response.data):
        image_data = b64decode(image_dict.b64_json)
        file_path = Path.cwd() / "output" / f"{response.created}_{index}.png"

        with open(file_path, "wb") as png:
            png.write(image_data)