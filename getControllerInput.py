import pygame

class ControllerManager:
    def __init__(self):
        self.initialized = False
        self.manette = None
        self.running = False
        self.button_states = {}
        self.axis_values = {}
    
    def initialize(self):
        """Initialise pygame et la manette"""
        pygame.init()
        pygame.joystick.init()
        
        # Vérifie si une manette est branchée
        if pygame.joystick.get_count() == 0:
            print("Aucune manette détectée. Branche une Xbox et relance.")
            return False
        
        # Prend la première manette dispo
        self.manette = pygame.joystick.Joystick(0)
        self.manette.init()
        self.initialized = True
        self.running = True
        
        print(f"Manette détectée : {self.manette.get_name()}")
        return True
    
    def update(self):
        """Met à jour les états des boutons et axes"""
        if not self.initialized:
            return False
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return False
                
            # Boutons pressés
            if event.type == pygame.JOYBUTTONDOWN:
                self.button_states[event.button] = True
                
            # Boutons relâchés
            if event.type == pygame.JOYBUTTONUP:
                self.button_states[event.button] = False
                
            # Joysticks et triggers
            if event.type == pygame.JOYAXISMOTION:
                self.axis_values[event.axis] = event.value
                
        return True
    
    def get_button(self, button_id):
        """Retourne l'état d'un bouton (True si pressé, False sinon)"""
        return self.button_states.get(button_id, False)
    
    def get_axis(self, axis_id):
        """Retourne la valeur brute d'un axe"""
        return self.axis_values.get(axis_id, 0.0)
    
    def get_trigger_percentage(self, axis_id):
        """Retourne la valeur d'un trigger en pourcentage (0-100%)"""
        if axis_id in [4, 5]:  # Les axes des triggers sur Xbox
            raw_value = self.get_axis(axis_id)
            return int((raw_value + 1) / 2 * 100)
        return 0
    
    def close(self):
        """Ferme proprement pygame"""
        self.running = False
        if self.initialized:
            pygame.quit()
            self.initialized = False

# Si le script est exécuté directement, tester la bibliothèque
if __name__ == "__main__":
    controller = ControllerManager()
    if controller.initialize():
        try:
            while controller.running:
                if controller.update():
                    # Afficher l'état des boutons pressés
                    for button_id, pressed in controller.button_states.items():
                        if pressed:
                            print(f"Bouton {button_id} pressé")
                    
                    # Afficher les valeurs des triggers en pourcentage
                    for axis_id in [4, 5]:
                        percentage = controller.get_trigger_percentage(axis_id)
                        if percentage > 0:
                            print(f"Bumper/Trigger axe {axis_id} : {percentage}%")
                
                pygame.time.delay(100)  # Petit délai pour ne pas surcharger le CPU
        finally:
            controller.close()
