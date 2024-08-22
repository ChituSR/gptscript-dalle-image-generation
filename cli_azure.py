import os
import sys
import argparse
import openai
from openai import AzureOpenAI

#from dotenv import load_dotenv

import os
import httpx
from openai import AzureOpenAI
from PIL import Image

API_VERSION="2024-04-01-preview"
client = AzureOpenAI(
    api_version="2024-02-01",  
    api_key=os.environ["AOAI_ENDPOINT"],  
    azure_endpoint=os.environ['AOAI_KEY']
)
      
# Set up defaults and get API key from environment variable
defaults = {
    "api_key": os.getenv('AOAI_KEY'),
    "model": "dall-e-3",#"gpt-4-vision",#"dall-e-3",
    "size": "1024x1024",
    "quality": "standard",
    "number": "1",
}
#load_dotenv(".env")
# create OpenAI client
base_url=os.environ.get("AOAI_ENDPOINT")
api_version= "2024-02-15-preview"
api_type= "azure"
api_key = os.environ.get("AOAI_KEY"),

# Function to validate and parse arguments
def validate_and_parse_args(parser):
    args = parser.parse_args()

    for key, value in vars(args).items():
        if not value:
            args.__dict__[key] = parser.get_default(key)

    if not args.api_key:
        parser.error('The --api-key argument is required if OPENAI_API_KEY environment variable is not set.')
    if not args.prompt:
        parser.error('The --prompt argument is required.')
    if not args.number.isdigit():
        parser.error('The --number argument must be a number.')
    args.number = int(args.number)

    return args

def main():
    # Parse the command line arguments
    parser = argparse.ArgumentParser(description="CLI for image generation prompt using OpenAI's DALL-E model.")
    parser.add_argument('-k', '--api-key', type=str, default=defaults["api_key"],
                        help='OpenAI API key. Can also be set with OPENAI_API_KEY environment variable.')
    parser.add_argument('-p', '--prompt', type=str, required=True, help='Prompt for image generation.')
    parser.add_argument('-m', '--model', type=str, default=defaults["model"],
                        help=f'Model to use for image generation. Default is "{defaults["model"]}".')
    parser.add_argument('-s', '--size', type=str, default=defaults["size"],
                        help=f'Size of the image to generate, format WxH (e.g. {defaults["size"]}). Default is {defaults["size"]}.')
    parser.add_argument('-q', '--quality', type=str, default=defaults["quality"],
                        help=f'Quality of the generated image. Allowed values are "standard" or "hd". Default is "{defaults["quality"]}"')
    parser.add_argument('-n', '--number', type=str, default=defaults["number"],
                        help='Number of images to generate. Default is 1.')
    args = validate_and_parse_args(parser)

 
    print("coming")
    client = AzureOpenAI(
    api_version="2024-02-01",  
    api_key=os.environ["AOAI_KEY"],  
    azure_endpoint=os.environ['AOAI_ENDPOINT']
)
    # Make request to the OpenAI API
    try:
        response = client.images.generate(
            model=args.model,
            prompt=args.prompt,
            size=args.size,
            quality=args.quality,
            n=args.number
        )
        print([image.url for image in response.data])
    except openai.OpenAIError as e:
        print(f"Received an error code while generating images: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
