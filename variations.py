import argparse
import json
import openai
from openai import OpenAI
from base64 import b64decode
from pathlib import Path

from utils import save_image, write_image_data_json

def parse_arguments():
    parser = argparse.ArgumentParser(description="Create variations of images generated using DALL·E")
    parser.add_argument("path", type=str, help="Path to the JSON file containing the image data.")
    parser.add_argument("--num-variations", type=int, default=3, help="Number of variations to create.")
    return parser.parse_args()

def create_variation(client, args):
    with open(args.path, "r", encoding="utf-8") as file:
        saved_response = json.load(file)
        image_data = b64decode(saved_response["data"][0]["b64_json"])

        try:
            response = client.images.create_variation(
                image=image_data,
                n=args.num_variations,
                size="256x256",
                response_format="b64_json"
            )
        except openai.OpenAIError as e:
            print(e)
    
    return response

def main():
    client = OpenAI()
    args = parse_arguments()
    response = create_variation(client, args)
    write_image_data_json(response)
    save_image(response)

if __name__ == "__main__":
    main()