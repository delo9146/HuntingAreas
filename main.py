import os
from hunting.ConfigManager import ConfigManager
from hunting.fileManager import fileManager
from hunting.imageAnalysis import ImageAnalysisManager
from hunting.waypointDrawer import WaypointDrawer

def main():
    print("🐾 Welcome to the Hunting Area Analyzer")
    species = input("Enter the species you're hunting (e.g., elk, black_bear, mule_deer): ").strip()

    try:
        # Load parts of the full prompt
        base_prompt = ConfigManager.load_species_prompt(species)
        legend_info = ConfigManager.get_map_legend_description()
        schema_prompt = ConfigManager.get_response_schema()

        # Combine into the full prompt
        full_prompt = f"{base_prompt.strip()}\n\n{legend_info.strip()}\n\n{schema_prompt.strip()}"

        print(f"\n Loaded prompt for '{species}'.\n")

        # Get image files from data/input
        image_paths = fileManager.get_input_images()
        if not image_paths:
            print("  No image files found in data/input. Add screenshots and try again.")
            return

        analyzer = ImageAnalysisManager()

        for image_path in image_paths:
            print(f" Processing image: {os.path.basename(image_path)}")

            try:
                # Step 1: Analyze with GPT-4 Vision
                gpt_response = analyzer.analyze_image(image_path, prompt=full_prompt)
                print(f" GPT Response for {os.path.basename(image_path)}:\n{gpt_response}\n{'-'*60}\n")

                # Step 2: Draw waypoints on the image
                output_image_path = WaypointDrawer.draw_waypoints(image_path, gpt_response)
                print(f" ✅ Marked-up map saved to: {output_image_path}\n")

            except Exception as e:
                print(f" ❌ Failed to process {image_path}: {e}")

    except ValueError as ve:
        print(f"\n {ve}")
    except Exception as e:
        print(f"\n Unexpected error: {e}")

if __name__ == "__main__":
    main()
