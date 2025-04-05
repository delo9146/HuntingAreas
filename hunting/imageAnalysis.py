# hunting/ImageAnalysisManager.py

import os
import base64
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class ImageAnalysisManager:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4o"  # or gpt-4-vision-preview if needed

    def encode_image_to_base64(self, image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")

    def analyze_image(self, image_path, prompt):
        image_b64 = self.encode_image_to_base64(image_path)
        image_data_url = f"data:image/png;base64,{image_b64}"

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
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
