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

        # Only accept wrapped "hunting_spots" format (grid-based POC only)
        if isinstance(parsed, dict) and "hunting_spots" in parsed:
            return parsed["hunting_spots"]

        raise ValueError("Expected JSON object with 'hunting_spots' key.")

    @staticmethod
    def draw_waypoints(image_path: str, gpt_response: str, output_dir: str = None) -> str:
        locations = WaypointDrawer.clean_and_parse_response(gpt_response)

        with Image.open(image_path) as img:
            draw = ImageDraw.Draw(img)
            width, height = img.size
            radius = 6
            grid_size = 20
            cell_width = width // grid_size
            cell_height = height // grid_size

            try:
                font = ImageFont.truetype("arial.ttf", 20)
            except IOError:
                font = ImageFont.load_default()

            for i, loc in enumerate(locations):
                grid_label = loc.get("grid_location")
                if not grid_label or len(grid_label) < 2:
                    continue

                row_letter = grid_label[0].upper()
                col_number = int(grid_label[1:])

                row_index = ord(row_letter) - ord("A")
                col_index = col_number - 1

                x = col_index * cell_width + cell_width // 2
                y = row_index * cell_height + cell_height // 2

                draw.ellipse([(x - radius, y - radius), (x + radius, y + radius)], fill="red", outline="black")
                draw.text((x + radius + 5, y - radius), f"{i + 1}", fill="red", font=font)

            base = os.path.basename(image_path)
            name, ext = os.path.splitext(base)

            if output_dir is None:
                output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "output")

            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, f"{name}_waypoints{ext}")
            img.save(output_path)

            return output_path
