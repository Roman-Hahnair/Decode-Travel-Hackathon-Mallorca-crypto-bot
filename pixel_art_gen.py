import openai
from PIL import Image
import requests
import os
from io import BytesIO

"""
Here we generate an unique pixel art image using the OpenAI API, to be used as the NFT image.
For that we use an API for the OpenAI DALL-E model, which is a powerful image generation model.
"""

# Get the OPEN API key
openai.api_key = os.getenv("OPENAI_API_KEY")


# Initialize the OpenAI client
client = openai.OpenAI()


def generate_image(object_to_paint):
    """Generates an arbitrary image using the DALL-E model.

    Args:
    object_to_paint (str): The thing to paint in the image. E.g. "ice cream"

    Returns:
    str: The URL of the generated image, hosted for a short time by OpenAI.
    """

    # Generate an image
    response = client.images.generate(
        model="dall-e-2",  # can be 3, but has different limitations
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
    """Fetches an image from a URL.

    Args:
    image_url (str): The URL of the image to fetch.

    Returns:
    Image: The fetched image.
    """
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))
    return img


def convert_to_pixel_art(image, new_size=(32, 32)):
    """Donwsize the image and convert it to pixel art.

    Args:
    image (Image): The image to convert.
    new_size (tuple): The new size of the image.

    Returns:
    Image: The converted image.
    
    """
    # Resize to a small dimension
    pixel_art = image.resize(new_size, resample=Image.NEAREST)
    pixel_art = pixel_art.quantize(colors=16)  # to enhance the pixel effect
    return pixel_art


def get_pixel_art(object_to_paint):
    """Generates a pixel art image of an object.

    Args:
    object_to_paint (str): The object to paint in the image. E.g. "ice cream".

    Returns:
    Image: The generated pixel art image.
    str: The URL of the original image.
    """
    original_image_url = generate_image(object_to_paint)
    image = fetch_image(original_image_url)
    pixel_art_image = convert_to_pixel_art(image)
    return pixel_art_image, original_image_url


def save_image(image, path):
    """Saves an image to a file.

    Args:
    image (Image): The image to save.
    path (str): The path to save the image to.
    """
    image.save(path)


def generate_and_save_pixel_art(object_to_paint, path="generated_image.png"):
    """Generates and saves a pixel art image of an object.

    Args:
    object_to_paint (str): The object to paint in the image. E.g. "ice cream".
    path (str): The path to save the image to.

    Returns:
    str: The URL of the original image (not downscaled).
    """
    pixel_art_image, original_image_url = get_pixel_art(object_to_paint)
    save_image(pixel_art_image, path)
    return original_image_url
