# hunting/WaypointDrawer.py

import os
import json
import re
from PIL import Image, ImageDraw, ImageFont

class WaypointDrawer:
    @staticmethod
    def clean_and_parse_response(gpt_response: str):
        cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", gpt_response.strip(), flags=re.IGNORECASE)
        try:
            parsed = json.loads(cleaned)
        except json.JSONDecodeError:
            raise ValueError("Failed to parse GPT response as JSON.")

        # Handle wrapped format like: {"hunting_spots": [...]}
        if isinstance(parsed, dict) and "hunting_spots" in parsed:
            return parsed["hunting_spots"]

        # Handle plain list format
        if isinstance(parsed, list):
            return parsed

        raise ValueError("Parsed response is not a list or a 'hunting_spots' dictionary.")

    @staticmethod
    def draw_waypoints(image_path: str, gpt_response: str, output_dir: str = None) -> str:
        locations = WaypointDrawer.clean_and_parse_response(gpt_response)

        with Image.open(image_path) as img:
            draw = ImageDraw.Draw(img)
            radius = 6

            # Load a default or system font
            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except IOError:
                font = ImageFont.load_default()

            for i, loc in enumerate(locations):
                coord = loc["coordinates"]
                if isinstance(coord, dict):
                    x, y = coord.get("x"), coord.get("y")
                elif isinstance(coord, list):
                    x, y = coord
                else:
                    continue

                draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill="red", outline="black")
                label = f"{i + 1}"
                draw.text((x + radius + 5, y - radius), label, fill="red", font=font)

            base = os.path.basename(image_path)
            name, ext = os.path.splitext(base)

            if output_dir is None:
                output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "output")

            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{name}_waypoints{ext}")
            img.save(output_path)

            return output_path
