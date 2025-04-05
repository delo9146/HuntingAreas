import os
from hunting.ConfigManager import ConfigManager
from hunting.fileManager import fileManager
from hunting.imageAnalysis import ImageAnalysisManager

def main():
    print("🐾 Welcome to the Hunting Area Analyzer")
    species = input("Enter the species you're hunting (e.g., elk, black_bear, mule_deer): ").strip()

    try:
        # Load species-specific prompt from config
        prompt = ConfigManager.load_species_prompt(species)
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
                result = analyzer.analyze_image(image_path, prompt=prompt)
                print(f" GPT Response for {os.path.basename(image_path)}:\n{result}\n{'-'*60}\n")
            except Exception as e:
                print(f" Failed to process {image_path}: {e}")

    except ValueError as ve:
        print(f"\n {ve}")
    except Exception as e:
        print(f"\n Unexpected error: {e}")

if __name__ == "__main__":
    main()
