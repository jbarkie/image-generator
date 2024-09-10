import openai
from openai import OpenAI
import argparse
from pathlib import Path
from base64 import b64decode

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate images using DALL·E")
    parser.add_argument("prompt", type=str, help="Image generation prompt")
    parser.add_argument("--model", type=str, default="dall-e-2", help="Model to use. Must be one of 'dall-e-2' or 'dall-e-3'.")
    parser.add_argument("--quality", type=str, default="standard", help="Image quality. Must be one of 'standard' or 'hd'.")
    parser.add_argument("--response-format", type=str, default="url", help="Response format. Must be one of 'url' or 'b64_json'.")
    parser.add_argument("--size", type=str, default="1024x1024", help="Image size. Must be one of 1024x1024, 1792x1024, or 1024x1792.")
    parser.add_argument("--style", type=str, default="vivid", help="Generated image style. Must be one of 'vivid' or 'natural'.")
    parser.add_argument("--output", type=str, default="output/image.png", help="Output file path.")
    return parser.parse_args()

def create_output_path(output_path):
    last_slash_index = output_path.rfind("/")
    output_dir = Path.cwd() if last_slash_index == -1 else Path.cwd() / output_path[:last_slash_index]
    output_dir.mkdir(exist_ok=True)

def generate_image(client, prompt, model, quality, response_format, size, style):
    try:
        response = client.images.generate(
            prompt=prompt,
            model=model,
            quality=quality,
            response_format=response_format,
            size=size,
            style=style,
        )
    except openai.OpenAIError as e:
        print(e.http_status)
        print(e.error)
    return response

def save_image(file_path, response):
    for _, image_dict in enumerate(response.data):
        image_data = b64decode(image_dict.b64_json)
        with open(file_path, "wb") as png:
            png.write(image_data)

def main():
    client = OpenAI()
    args = parse_arguments()
    create_output_path(args.output)
    response = generate_image(client, args.prompt,
     args.model, args.quality, args.response_format, args.size, args.style)
    if args.response_format == "b64_json":
        save_image(args.output, response)
    else:
        print(f"Access image for up to one hour at the following URL: {response.data[0].url}")

if __name__ == "__main__":
    main()