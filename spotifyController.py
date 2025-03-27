import time
import subprocess
import os
import sys
from getControllerInput import ControllerManager

# Vérifier si le module est installé, sinon l'installer
try:
    import psutil
except ImportError:
    print("Installation du module psutil...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
    import psutil

def is_spotify_running():
    """Vérifie si Spotify est en cours d'exécution"""
    for proc in psutil.process_iter(['name']):
        if 'spotify' in proc.info['name'].lower():
            return True
    return False

def send_media_key(key_code):
    """Envoie une commande multimédia à Windows"""
    try:
        # Nécessite le module pyautogui pour les touches multimédias
        import pyautogui
    except ImportError:
        print("Installation du module pyautogui...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyautogui"])
        import pyautogui
    
    # Envoi d'un raccourci clavier multimédia
    if key_code == 'play_pause':
        pyautogui.press('playpause')
    elif key_code == 'next':
        pyautogui.press('nexttrack')
    elif key_code == 'previous':
        pyautogui.press('prevtrack')
    elif key_code == 'volume_up':
        pyautogui.press('volumeup')
    elif key_code == 'volume_down':
        pyautogui.press('volumedown')

def main():
    # Vérifier si Spotify est installé et en cours d'exécution
    if not is_spotify_running():
        print("Spotify n'est pas en cours d'exécution. Veuillez lancer Spotify d'abord.")
        # Option: on pourrait ajouter du code pour lancer Spotify ici
        return
    
    print("Spotify détecté! Contrôle via manette activé.")
    
    # Initialiser le gestionnaire de manette
    controller = ControllerManager()
    if not controller.initialize():
        print("Impossible d'initialiser la manette")
        return
    
    # Mapping des boutons (pour Xbox):
    # Bouton A (0) : Play/Pause
    # Bouton B (1) : Piste suivante
    # Bouton X (2) : Piste précédente
    # LT (4) et RT (5) : Volume down/up
    
    # Pour éviter les actions répétées, on garde trace des états précédents
    previous_states = {
        'A': False,
        'B': False, 
        'X': False,
        'LT': 0,
        'RT': 0
    }
    
    print("Contrôle Spotify avec manette:")
    print("- A: Play/Pause")
    print("- B: Piste suivante")
    print("- X: Piste précédente")
    print("- LT: Baisser volume")
    print("- RT: Augmenter volume")
    print("Appuyez sur Ctrl+C pour quitter")
    
    try:
        while controller.running:
            controller.update()
            
            # Play/Pause (bouton A)
            if controller.get_button(0) and not previous_states['A']:
                print("Play/Pause")
                send_media_key('play_pause')
            previous_states['A'] = controller.get_button(0)
            
            # Piste suivante (bouton B)
            if controller.get_button(1) and not previous_states['B']:
                print("Piste suivante")
                send_media_key('next')
            previous_states['B'] = controller.get_button(1)
            
            # Piste précédente (bouton X)
            if controller.get_button(2) and not previous_states['X']:
                print("Piste précédente")
                send_media_key('previous')
            previous_states['X'] = controller.get_button(2)
            
            # Contrôle du volume avec les triggers
            lt_value = controller.get_trigger_percentage(4)
            rt_value = controller.get_trigger_percentage(5)
            
            # Volume - (LT)
            if lt_value > 50 and previous_states['LT'] <= 50:
                print("Volume -")
                send_media_key('volume_down')
            previous_states['LT'] = lt_value
            
            # Volume + (RT)
            if rt_value > 50 and previous_states['RT'] <= 50:
                print("Volume +")
                send_media_key('volume_up')
            previous_states['RT'] = rt_value
            
            time.sleep(0.1)  # Pour éviter de surcharger le CPU
            
    except KeyboardInterrupt:
        print("\nProgramme arrêté par l'utilisateur")
    finally:
        controller.close()

if __name__ == "__main__":
    main()
