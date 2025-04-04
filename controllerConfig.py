import os
import json

DEFAULT_CONFIG = {
    "activation": {
        "buttons": {
            "X": 2,
            "A": 0,
            "R3": 8
        },
        "combo": [2, 0, 8]  # Activation: X, A, R3
    },
    "spotify_controls": {
        "skip": 1,           # Bouton B pour skipper la musique
        "prev": 2,           # Bouton X pour revenir à la musique précédente
        "play_pause": 0,     # Bouton A pour play/pause
        "volume_up": 5,
        "volume_down": 4
    }
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

def get_activation_combo():
    """Retourne la combo d'activation de l'overlay."""
    config = load_config()
    return config.get("activation", DEFAULT_CONFIG["activation"]).get("combo", DEFAULT_CONFIG["activation"]["combo"])

def get_activation_buttons():
    """Retourne les boutons utilisés pour activer l'overlay."""
    config = load_config()
    return config.get("activation", DEFAULT_CONFIG["activation"]).get("buttons", DEFAULT_CONFIG["activation"]["buttons"])

def get_spotify_controls():
    """Retourne les boutons dédiés au contrôle de Spotify."""
    config = load_config()
    return config.get("spotify_controls", DEFAULT_CONFIG["spotify_controls"])
