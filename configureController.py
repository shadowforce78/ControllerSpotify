import os
import json
import time
import sys
from getControllerInput import ControllerManager

def clear_screen():
    """Clear the terminal screen based on OS"""
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Main function to configure controller inputs and save to JSON"""
    print("=== Configuration de la manette pour Spotify Controller ===")
    print("\nCe programme va vous aider à configurer les boutons de votre manette.")
    
    # Initialize controller
    controller = ControllerManager()
    if not controller.initialize():
        print("Impossible d'initialiser la manette. Vérifiez qu'elle est bien connectée.")
        sys.exit(1)
    
    print("\nManette détectée ! Commençons la configuration...")
    
    # Config dictionary to store button mappings
    config = {
        "buttons": {},
        "combo": []
    }
    
    # Test buttons to identify them
    print("\n=== TEST DES BOUTONS ===")
    print("Appuyez sur les boutons de votre manette un par un pour voir leur ID")
    print("Appuyez sur CTRL+C pour terminer le test")
    
    try:
        while True:
            controller.update()
            for button_id in range(15):  # Most controllers have less than 15 buttons
                if controller.get_button(button_id):
                    print(f"Bouton pressé: ID {button_id}")
                    time.sleep(0.3)  # Prevent multiple detections of the same press
    except KeyboardInterrupt:
        print("\nTest des boutons terminé.")
    
    # Configure overlay activation combo
    print("\n=== CONFIGURATION DU COMBO D'ACTIVATION ===")
    print("Vous allez maintenant configurer la combinaison de boutons pour afficher/masquer l'overlay Spotify.")
    
    combo_buttons = []
    button_names = {}
    
    while True:
        button_name = input("\nDonnez un nom au bouton à ajouter (ex: X, A, R3) ou tapez 'fin' pour terminer: ")
        if button_name.lower() == 'fin':
            break
        
        try:
            button_id = int(input(f"Entrez l'ID du bouton '{button_name}' (vu lors du test): "))
            combo_buttons.append(button_id)
            button_names[button_id] = button_name
            config["buttons"][button_name] = button_id
            
            print(f"Bouton '{button_name}' (ID: {button_id}) ajouté à la combinaison!")
        except ValueError:
            print("Erreur: veuillez entrer un nombre entier pour l'ID du bouton.")
    
    config["combo"] = combo_buttons
    
    # Save configuration to JSON file
    config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "controller_config.json")
    with open(config_path, "w") as config_file:
        json.dump(config, config_file, indent=4)
    
    print(f"\nConfiguration sauvegardée dans {config_path}")
    print("\nRécapitulatif de la configuration:")
    print(f"Combinaison d'activation: {', '.join([button_names[btn_id] for btn_id in combo_buttons])}")
    
    controller.close()
    print("\nConfiguration terminée. Vous pouvez maintenant utiliser spotifyController.py")

if __name__ == "__main__":
    main()
