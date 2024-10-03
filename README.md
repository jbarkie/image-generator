# DALL·E CLI for AI Image Generation

This Python program uses the OpenAI API and DALL·E to generate images via an easy-to-use CLI.

## Installation

- Clone the repository
- Ensure that you have your [OpenAI API key set in your environment variables.](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety)
- Create a new virtual environment:
  `python3 -m venv venv`
- Activate the virtual environment:
  `source venv/bin/activate`
- Install required dependencies:
  `pip install -r requirements.txt`
- Run the script: `python3 generate.py "A vaporwave skateboard."`
- Inspect the output.

## Features

### Image Generation

- Make a request to the image generations endpoint to create an original image given a text prompt. 

```bash
python3 generate.py --model="dall-e-3" --quality="hd" --response-format="b64_json" --size="1024x1792" --style="natural" --output="output" "A dancing leprechaun holding a pint"
```

### Variations

- Make a request to the image variations endpoint to generate a variation of a given image that is a square PNG less than 4MB in size.

```bash
python3 variations.py --num-variations=1 --output="output" "/image/data/json/path/"
```
