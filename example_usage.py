
from getControllerInput import ControllerManager
import time

# Créer et initialiser le gestionnaire de manette
controller = ControllerManager()
if not controller.initialize():
    print("Impossible d'initialiser la manette")
    exit()

try:
    # Boucle principale
    while controller.running:
        # Mettre à jour l'état de la manette
        controller.update()
        
        # Exemples d'utilisation
        if controller.get_button(0):  # Bouton A sur Xbox
            print("Bouton A pressé!")
            
        left_trigger = controller.get_trigger_percentage(4)
        right_trigger = controller.get_trigger_percentage(5)
        
        if left_trigger > 50:
            print(f"Trigger gauche pressé à {left_trigger}%")
            
        if right_trigger > 50:
            print(f"Trigger droit pressé à {right_trigger}%")
            
        time.sleep(0.1)  # Pour éviter de surcharger le CPU
            
except KeyboardInterrupt:
    print("Programme arrêté par l'utilisateur")
finally:
    # Fermeture propre
    controller.close()