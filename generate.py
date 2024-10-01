import openai
from openai import OpenAI
import argparse
from pathlib import Path

from utils import save_image, write_image_data_json

def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate images using DALL·E")
    parser.add_argument("prompt", type=str, help="Image generation prompt")
    parser.add_argument("--model", type=str, default="dall-e-2", choices=["dall-e-2", "dall-e-3"], help="Model to use. Must be one of 'dall-e-2' or 'dall-e-3'.")
    parser.add_argument("--num-images", type=int, help="Number of images to generate. For dall-e-3, only 1 image can be generated.")
    parser.add_argument("--quality", type=str, choices=["standard", "hd"] ,help="Image quality. Must be one of 'standard' or 'hd'.")
    parser.add_argument("--response-format", type=str, default="url", choices=["url", "b64_json"], help="Response format. Must be one of 'url' or 'b64_json'.")
    parser.add_argument("--size", type=str, default="1024x1024", choices=["256x256", "512x512", "1024x1024", "1792x1024", "1024x1792"], help="Image size. Must be one of 256x256, 512x512, or 1024x1024 for dall-e-2. Must be one of 1024x1024, 1792x1024, or 1024x1792 for dall-e-3.")
    parser.add_argument("--style", type=str, choices=["vivid", "natural"], help="Generated image style. Must be one of 'vivid' or 'natural'.")
    parser.add_argument("--output", type=str, default="output/image", help="Output file path.")
    return parser

def validate_arguments(args, parser):
    # Validate num_images argument
    if args.num_images is None:
        args.num_images = 1 # default number of images
    if args.model == "dall-e-3" and args.num_images != 1:
        parser.error("When using the dall-e-3 model, only one image can be generated at a time.")

    # Validate quality argument
    if args.quality is None and args.model == "dall-e-3":
        args.quality = "standard" # default quality
    if args.quality is not None and args.model != "dall-e-3":
        parser.error("The 'quality' argument is only supported for the dall-e-3 model.")

    # Validate size argument
    DALLE_2_SIZES = ["256x256", "512x512", "1024x1024"]
    DALLE_3_SIZES = ["1024x1024", "1792x1024", "1024x1792"]
    if args.model == "dall-e-2" and args.size not in DALLE_2_SIZES:
        parser.error(f"The 'size' argument must be one of {DALLE_2_SIZES} for the dall-e-2 model.")
    if args.model == "dall-e-3" and args.size not in DALLE_3_SIZES:
        parser.error(f"The 'size' argument must be one of {DALLE_3_SIZES} for the dall-e-3 model.")

    # Validate style argument
    if args.style is None and args.model == "dall-e-3":
        args.style = "vivid" # default style
    if args.style is not None and args.model != "dall-e-3":
        parser.error("The 'style' argument is only supported for the dall-e-3 model.")

    return args

def assemble_args_for_model(args):
    kwargs = {
        "prompt": args.prompt,
        "model": args.model,
        "n": args.num_images,
        "response_format": args.response_format,
        "size": args.size,
    }
    if args.model == "dall-e-3":
        kwargs["quality"] = args.quality
        kwargs["style"] = args.style
    return kwargs

def create_output_path(output_path):
    last_slash_index = output_path.rfind("/")
    output_dir = Path.cwd() if last_slash_index == -1 else Path.cwd() / output_path[:last_slash_index]
    output_dir.mkdir(exist_ok=True)

def generate_image(client, kwargs):
    try:
        response = client.images.generate(**kwargs)
    except openai.OpenAIError as e:
        print(e.http_status)
        print(e.error)
    return response

def main():
    client = OpenAI()
    parser = parse_arguments()
    args = validate_arguments(parser.parse_args(), parser)
    create_output_path(args.output)
    kwargs = assemble_args_for_model(args)
    response = generate_image(client, kwargs)
    if args.response_format == "b64_json":
        json_path = write_image_data_json(response)
        save_image(response, args.output)
        print(json_path)
    else:
        print(f"Access image for up to one hour at the following URL: {response.data[0].url}")

if __name__ == "__main__":
    main()