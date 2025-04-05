import os
import tomli

class ConfigManager:
    @staticmethod
    def load_species_prompt(species: str, config_path: str = None) -> str:
        if config_path is None:
            base_path = os.path.dirname(os.path.dirname(__file__))  # go up from /hunting
            config_path = os.path.join(base_path, "config", "hunting.toml")

        with open(config_path, "rb") as f:
            config = tomli.load(f)

        species_lower = species.lower()
        if species_lower not in config:
            raise ValueError(f"Species '{species}' not found in config.")

        return config[species_lower]["prompt"]
