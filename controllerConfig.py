import os
import json

DEFAULT_CONFIG = {
    "buttons": {
        "X": 2,
        "A": 0,
        "R3": 8
    },
    "combo": [2, 0, 8]  # X, A, R3
}

def load_config():
    """
    Load controller configuration from JSON file or return default config if file doesn't exist
    
    Returns:
        dict: Configuration dictionary with button mappings and combo
    """
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "controller_config.json")
    
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as config_file:
                return json.load(config_file)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Erreur lors du chargement de la configuration: {e}")
            print("Utilisation de la configuration par défaut.")
            return DEFAULT_CONFIG
    else:
        print("Fichier de configuration non trouvé. Utilisation de la configuration par défaut.")
        return DEFAULT_CONFIG

def get_button_ids():
    """
    Get the button IDs for the overlay activation combo
    
    Returns:
        list: List of button IDs used in the activation combo
    """
    config = load_config()
    return config.get("combo", DEFAULT_CONFIG["combo"])

def get_button_names():
    """
    Get button names mapped to their IDs
    
    Returns:
        dict: Dictionary mapping button names to IDs
    """
    config = load_config()
    return config.get("buttons", DEFAULT_CONFIG["buttons"])
