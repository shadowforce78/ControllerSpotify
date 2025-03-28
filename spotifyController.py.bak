import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
from getControllerInput import ControllerManager  # Ton script de gestion de manette

# Charger les variables d'environnement
load_dotenv()

# Initialiser l'authentification Spotify
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-modify-playback-state,user-read-playback-state"
))

def play_pause():
    """Joue ou met en pause Spotify"""
    playback = sp.current_playback()
    if playback and playback["is_playing"]:
        sp.pause_playback()
        print("Pause")
    else:
        sp.start_playback()
        print("Play")

def next_track():
    """Passe à la musique suivante"""
    sp.next_track()
    print("Piste suivante")

def previous_track():
    """Revient à la musique précédente"""
    sp.previous_track()
    print("Piste précédente")

def volume_up():
    """Augmente le volume"""
    playback = sp.current_playback()
    if playback:
        new_volume = min(playback["device"]["volume_percent"] + 10, 100)
        sp.volume(new_volume)
        print(f"Volume : {new_volume}%")

def volume_down():
    """Baisse le volume"""
    playback = sp.current_playback()
    if playback:
        new_volume = max(playback["device"]["volume_percent"] - 10, 0)
        sp.volume(new_volume)
        print(f"Volume : {new_volume}%")

def main():
    print("Spotify détecté! Contrôle via manette activé.")

    controller = ControllerManager()
    if not controller.initialize():
        print("Impossible d'initialiser la manette")
        return

    previous_states = {'A': False, 'B': False, 'X': False, 'LT': 0, 'RT': 0}

    try:
        while controller.running:
            controller.update()

            if controller.get_button(0) and not previous_states['A']:
                play_pause()
            previous_states['A'] = controller.get_button(0)

            if controller.get_button(1) and not previous_states['B']:
                next_track()
            previous_states['B'] = controller.get_button(1)

            if controller.get_button(2) and not previous_states['X']:
                previous_track()
            previous_states['X'] = controller.get_button(2)

            lt_value = controller.get_trigger_percentage(4)
            rt_value = controller.get_trigger_percentage(5)

            if lt_value > 50 and previous_states['LT'] <= 50:
                volume_down()
            previous_states['LT'] = lt_value

            if rt_value > 50 and previous_states['RT'] <= 50:
                volume_up()
            previous_states['RT'] = rt_value

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nProgramme arrêté")
    finally:
        controller.close()

if __name__ == "__main__":
    main()
