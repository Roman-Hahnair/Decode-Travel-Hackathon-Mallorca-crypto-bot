import openai
from PIL import Image
import requests
import os
from io import BytesIO

# Set your API key
openai.api_key = os.getenv('OPENAI_API_KEY')


# Initialize the OpenAI client
client = openai.OpenAI()


def generate_image(object_to_paint):
    # object_to_paint = "ice cream"

    # Generate an image
    response = client.images.generate(
        model="dall-e-2", # can be 3
        prompt=f"a detailed pixel art of a {object_to_paint} on a Mallorca beach",
        size="256x256",
        quality="standard",
        n=1,
    )

    # Extract the URL of the generated image
    image_url = response.data[0].url

    # Print the image URL
    print(image_url)
    return image_url

def fetch_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    return img

def convert_to_pixel_art(image, new_size=(32, 32)):
    # Resize to a small dimension
    pixel_art = image.resize(new_size, resample=Image.NEAREST)
    # Optional: reduce color palette
    pixel_art = pixel_art.quantize(colors=16)  # Reduce colors to enhance the pixel art effect
    return pixel_art


# img.show()


# pixel_art_image.show()

def get_pixel_art(object_to_paint):
    original_image_url = generate_image(object_to_paint)
    image = fetch_image(original_image_url)
    pixel_art_image = convert_to_pixel_art(image)
    return pixel_art_image, original_image_url


def save_image(image, path):
    image.save(path)

# Optionally, save the image locally
# pixel_art_image.save("generated_image.png")

def generate_and_save_pixel_art(object_to_paint, path="generated_image.png"):
    pixel_art_image, original_image_url = get_pixel_art(object_to_paint)
    save_image(pixel_art_image, path)
    # pixel_art_image.show()
    return original_image_url


# generate_and_save_pixel_art("funny dog", "generated_image.png")