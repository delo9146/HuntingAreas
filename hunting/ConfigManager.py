import toml
import os

class ConfigManager:
    CONFIG_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config", "hunting.toml")

    @staticmethod
    def load_species_prompt(species: str) -> str:
        if not os.path.exists(ConfigManager.CONFIG_PATH):
            raise ValueError("Missing hunting.toml config file.")

        config = toml.load(ConfigManager.CONFIG_PATH)
        if species not in config:
            raise ValueError(f"No prompt found for species '{species}' in hunting.toml")

        return config[species]["prompt"]
    
    @staticmethod
    def get_full_state_name(state_abbr: str) -> str:
        config = toml.load(ConfigManager.CONFIG_PATH)
        states = config.get("states", {})
        full_name = states.get(state_abbr.upper())

        if not full_name:
            raise ValueError(f"Unknown state abbreviation '{state_abbr}' in hunting.toml")

        return full_name


    @staticmethod
    def get_response_schema() -> str:
        return (
            "Respond only with JSON in the following format:\n\n"
            "{\n"
            '  "hunting_spots": [\n'
            "    {\n"
            '      "description": "Detailed rationale for why this is a good location.",\n'
            '      "grid_location": "A1"  // Row letter and column number\n'
            "    },\n"
            "    ... (3 total spots)\n"
            "  ]\n"
            "}\n\n"
            "Do not include any explanation or text outside of the JSON block."
        )

    
    @staticmethod
    def get_map_legend_description() -> str:
        config = toml.load(ConfigManager.CONFIG_PATH)
        if "map_legend" not in config:
            return ""

        legend_lines = [
            f"- {color}: {desc}" for color, desc in config["map_legend"].items()
        ]
        return "The map uses the following color-coded legend:\n" + "\n".join(legend_lines)

