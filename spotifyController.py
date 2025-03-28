import sys
import os
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from getControllerInput import ControllerManager
from dotenv import load_dotenv
from controllerConfig import load_config, get_button_ids, get_button_names

# Charger les variables Spotify
load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIPY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
    scope="user-modify-playback-state,user-read-playback-state"
))

class SpotifyOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Spotify Overlay")
        self.setGeometry(100, 100, 300, 200)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.X11BypassWindowManagerHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # Fond semi-transparent
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0, 180))
        self.setPalette(palette)

        layout = QVBoxLayout()

        # Labels pour afficher les informations
        self.track_label = QLabel("Aucune musique", self)
        self.track_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        layout.addWidget(self.track_label)
        
        # Spacer
        layout.addSpacing(10)
        
        # Ajouter des labels pour les contrôles (non interactifs)
        controls_info = [
            "🎮 Contrôles:",
            "⏯️ Play/Pause",
            "⏭️ Piste Suivante",
            "⏮️ Piste Précédente",
            "🔊 Volume +",
            "🔉 Volume -",
        ]
        
        for info in controls_info:
            label = QLabel(info, self)
            label.setStyleSheet("color: white; font-size: 14px;")
            layout.addWidget(label)
        
        # Note de fermeture
        close_label = QLabel("Utilisez la même combinaison de touches pour fermer", self)
        close_label.setStyleSheet("color: #aaaaaa; font-size: 12px; font-style: italic;")
        layout.addWidget(close_label)
        
        self.setLayout(layout)
        self.hide()  # On cache l'overlay au démarrage
        
        # Empêcher les interactions à la souris
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)

    def update_track_info(self):
        """Met à jour le nom de la musique en cours"""
        playback = sp.current_playback()
        if playback and "item" in playback and playback["item"]:
            track = playback["item"]["name"]
            artist = playback["item"]["artists"][0]["name"]
            self.track_label.setText(f"▶️ {track} - {artist}")
        else:
            self.track_label.setText("Aucune musique")

    # Supprimer les méthodes obsolètes liées aux boutons
    def toggle_overlay(self):
        if self.isVisible():
            print("Fermeture de l'overlay")
            self.hide()
        else:
            print("Affichage de l'overlay Spotify")
            self.update_track_info()
            self.show()

class ControllerListener:
    def __init__(self, overlay):
        self.overlay = overlay
        self.controller = ControllerManager()
        
        # Charger la configuration des boutons
        self.config = load_config()
        self.button_ids = get_button_ids()  # Liste des IDs de boutons pour le combo
        self.button_names = get_button_names()  # Dictionnaire nom -> ID

        if not self.controller.initialize():
            print("Impossible d'initialiser la manette")
            sys.exit(1)

    def listen(self):
        """Écoute la manette et affiche/ferme l'overlay si la combinaison configurée est pressée"""
        # Initialiser l'état précédent de chaque bouton
        prev_states = {name: False for name in self.button_names.keys()}
        
        try:
            while True:
                self.controller.update()
                
                # Récupérer l'état actuel de chaque bouton configuré
                current_states = {}
                for name, button_id in self.button_names.items():
                    current_states[name] = self.controller.get_button(button_id)
                
                # Afficher l'état des boutons pour le débogage
                states_str = ", ".join([f"{name}={state}" for name, state in current_states.items()])
                print(f"Boutons pressés: {states_str}")
                
                # Vérifier si tous les boutons de la combinaison sont pressés
                all_pressed = all(current_states.values())
                all_were_pressed = all(prev_states.values())
                
                # Afficher/masquer l'overlay si la combinaison est nouvellement pressée
                if all_pressed and not all_were_pressed:
                    self.overlay.toggle_overlay()
                
                # Mettre à jour l'état précédent
                prev_states = current_states.copy()
                
                time.sleep(0.1)

        except KeyboardInterrupt:
            print("Arrêt du programme")
        finally:
            self.controller.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    overlay = SpotifyOverlay()
    listener = ControllerListener(overlay)

    # Lancer l'écoute de la manette dans un thread séparé
    import threading
    listener_thread = threading.Thread(target=listener.listen, daemon=True)
    listener_thread.start()

    sys.exit(app.exec())
