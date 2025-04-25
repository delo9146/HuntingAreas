# hunting/imageEditManager.py

import os
import json
import re
from PIL import Image, ImageDraw
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ImageEditManager:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "dall-e-2"

    def generate_mask_from_coordinates(self, image_path: str, gpt_response: str) -> str:
        """Create a transparent PNG mask with opaque spots where red dots should go"""

        # Clean GPT response (strip ```json ... ```)
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", gpt_response.strip(), flags=re.IGNORECASE)

        try:
            coords = json.loads(cleaned)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in GPT response")

        # Load the base image to match mask size
        with Image.open(image_path) as img:
            width, height = img.size
            mask = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # fully transparent
            draw = ImageDraw.Draw(mask)

            for loc in coords:
                coord = loc["coordinates"]
                if isinstance(coord, dict):
                    x, y = coord.get("x"), coord.get("y")
                elif isinstance(coord, list) and len(coord) == 2:
                    x, y = coord
                else:
                    raise ValueError("Invalid coordinate format in GPT response")

                radius = 15
                draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill=(255, 255, 255, 255))

            # Save mask
            mask_path = os.path.splitext(image_path)[0] + "_mask.png"
            mask.save(mask_path)
            return mask_path

    def call_dalle_edit(self, image_path: str, mask_path: str, prompt: str) -> str:
        """Call the DALL·E edit endpoint and return the URL of the edited image"""
        with open(image_path, "rb") as image_file, open(mask_path, "rb") as mask_file:
            response = self.client.images.edit(
                image=image_file,
                mask=mask_file,
                prompt=prompt,
                model=self.model,
                n=1,
                size="1024x1024",
                response_format="url"
            )

        image_url = response.data[0].url
        return image_url
