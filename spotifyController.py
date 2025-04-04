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
from controllerConfig import (
    load_config,
    get_activation_buttons,
    get_activation_combo,
    get_spotify_controls,
)

# Charger les variables Spotify
load_dotenv()

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope="user-modify-playback-state,user-read-playback-state",
    )
)


class SpotifyOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Spotify Overlay")
        self.setGeometry(100, 100, 300, 200)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Fond semi-transparent
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0, 180))
        self.setPalette(palette)

        layout = QVBoxLayout()

        # Labels pour afficher les informations
        self.track_label = QLabel("Aucune musique", self)
        self.track_label.setStyleSheet(
            "color: white; font-size: 16px; font-weight: bold;"
        )
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
        close_label = QLabel(
            "Utilisez la même combinaison de touches pour fermer", self
        )
        close_label.setStyleSheet(
            "color: #aaaaaa; font-size: 12px; font-style: italic;"
        )
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

        # Charger les configurations séparées
        self.activation_buttons = get_activation_buttons()  # pour activer l'overlay
        self.spotify_controls = get_spotify_controls()  # pour contrôler Spotify

        # Initialiser les états précédents pour chaque groupe
        self.prev_activation_states = {
            name: False for name in self.activation_buttons.keys()
        }
        self.prev_spotify_states = {key: False for key in self.spotify_controls.keys()}

        if not self.controller.initialize():
            print("Impossible d'initialiser la manette")
            sys.exit(1)

    def listen(self):
        """Écoute la manette et gère l'activation de l'overlay ainsi que les commandes skip/précédent quand l'overlay est visible."""
        try:
            while True:
                self.controller.update()

                # Gestion du combo d'activation
                current_activation = {
                    name: self.controller.get_button(button_id)
                    for name, button_id in self.activation_buttons.items()
                }
                if all(current_activation.values()) and not all(self.prev_activation_states.values()):
                    self.overlay.toggle_overlay()
                    # Réinitialiser les états des boutons Spotify pour éviter un déclenchement non voulu
                    self.prev_spotify_states = {key: False for key in self.spotify_controls.keys()}
                self.prev_activation_states = current_activation.copy()

                # Si l'overlay est visible, gérer les commandes Spotify
                if self.overlay.isVisible():
                    # Utiliser les IDs définis dans spotify_controls
                    current_skip = self.controller.get_button(
                        self.spotify_controls["skip"]
                    )
                    if current_skip and not self.prev_spotify_states["skip"]:
                        print("Skip track")
                        sp.next_track()
                        self.overlay.update_track_info()

                    current_prev = self.controller.get_button(
                        self.spotify_controls["prev"]
                    )
                    if current_prev and not self.prev_spotify_states["prev"]:
                        print("Piste précédente")
                        sp.previous_track()
                        self.overlay.update_track_info()

                    self.prev_spotify_states["skip"] = current_skip
                    self.prev_spotify_states["prev"] = current_prev

                # ...existing delay...
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
