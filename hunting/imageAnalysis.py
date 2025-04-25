# hunting/ImageAnalysisManager.py

import os
import base64
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ImageAnalysisManager:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o"  # or gpt-4-vision-preview if you're testing that

    def encode_image_to_base64(self, image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")

    def get_image_dimensions(self, image_path):
        with Image.open(image_path) as img:
            return img.size  # (width, height)

    def analyze_image(self, image_path, prompt):
        width, height = self.get_image_dimensions(image_path)
        image_b64 = self.encode_image_to_base64(image_path)
        image_data_url = f"data:image/png;base64,{image_b64}"

        # Extend the prompt with dimensions
        prompt += f"\n\nThe image resolution is {width}x{height} pixels. Return 3 hunting spots with descriptions and estimated pixel coordinates (x, y). Format your response as JSON. Make sure to provide descriptions of the areas you chose and why you chose them."

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": ("You are a seasoned hunting guide skilled at analyzing maps to find optimal game locations."
                                "Assume map orientation is standard: North is up, South is down, East is right, and West is left. "
                    )
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image_url", "image_url": {"url": image_data_url}},
                    ],
                }
            ],
            max_tokens=1000,
        )

        return response.choices[0].message.content
