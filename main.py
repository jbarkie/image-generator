import openai
from openai import OpenAI
import argparse
from pathlib import Path
from base64 import b64decode

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate images using DALL·E")
    parser.add_argument("prompt", type=str, help="Image generation prompt")
    parser.add_argument("--model", type=str, default="dall-e-2", choices=["dall-e-2", "dall-e-3"], help="Model to use. Must be one of 'dall-e-2' or 'dall-e-3'.")
    parser.add_argument("--num-images", type=int, help="Number of images to generate. For dall-e-3, only 1 image can be generated.")
    parser.add_argument("--quality", type=str, default="standard", choices=["standard", "hd"] ,help="Image quality. Must be one of 'standard' or 'hd'.")
    parser.add_argument("--response-format", type=str, default="url", choices=["url", "b64_json"], help="Response format. Must be one of 'url' or 'b64_json'.")
    parser.add_argument("--size", type=str, default="1024x1024", choices=["1024x1024", "1792x1024", "1024x1792"], help="Image size. Must be one of 1024x1024, 1792x1024, or 1024x1792.")
    parser.add_argument("--style", type=str, default="vivid", choices=["vivid", "natural"], help="Generated image style. Must be one of 'vivid' or 'natural'.")
    parser.add_argument("--output", type=str, default="output/image.png", help="Output file path.")
    return parser

def validate_arguments(args, parser):
    if args.num_images is None:
        args.num_images = 1
    if args.model == "dall-e-3" and args.num_images != 1:
        parser.error("When using the dall-e-3 model, only one image can be generated at a time.")
    return args

def create_output_path(output_path):
    last_slash_index = output_path.rfind("/")
    output_dir = Path.cwd() if last_slash_index == -1 else Path.cwd() / output_path[:last_slash_index]
    output_dir.mkdir(exist_ok=True)

def generate_image(client, prompt, model, num_images, quality, response_format, size, style):
    try:
        response = client.images.generate(
            prompt=prompt,
            model=model,
            n=num_images,
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
    parser = parse_arguments()
    args = validate_arguments(parser.parse_args(), parser)
    create_output_path(args.output)
    response = generate_image(client, args.prompt,
     args.model, args.num_images, args.quality, args.response_format, args.size, args.style)
    if args.response_format == "b64_json":
        save_image(args.output, response)
    else:
        print(f"Access image for up to one hour at the following URL: {response.data[0].url}")

if __name__ == "__main__":
    main()