import pygame
import os
import sys  # Pour utiliser sys.exit()

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 215, 0)
GRAY = (100, 100, 100)

class Menu:
    """
    Classe pour gérer le menu principal.
    """
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 80)  # Police pour le titre
        self.font_option = pygame.font.Font(None, 50)  # Police pour les options
        self.selected_option = "START"  # Option par défaut

        # Charger l'image de fond
        try:
            path = os.path.join("assets", "background.jpg")  # Chemin attendu
            self.background = pygame.image.load(path)
            # Redimensionner l'image à la taille de l'écran
            screen_width, screen_height = self.screen.get_size()
            self.background = pygame.transform.scale(self.background, (screen_width, screen_height))
        except FileNotFoundError:
            print(f"Erreur : L'image 'background.jpg' est introuvable.")
            print(f"Chemin absolu recherché : {os.path.abspath(path)}")
            sys.exit()

        # Charger la musique de fond
        try:
            pygame.mixer.music.load(os.path.join("assets", "menu_music.mp3"))
            pygame.mixer.music.play(-1)  # Lecture en boucle
        except FileNotFoundError:
            print("Erreur : La musique 'menu_music.mp3' est introuvable.")
            sys.exit()

    def show_menu(self):
        """
        Affiche le menu et gère les interactions.
        """
        clock = pygame.time.Clock()

        while True:
            # Afficher l'image de fond
            self.screen.blit(self.background, (0, 0))

            # Affiche le titre
            title_text = self.font_title.render("Draconic Generations", True, YELLOW)
            self.screen.blit(title_text, (self.screen.get_width() // 2 - title_text.get_width() // 2, 100))

            # Affiche les options START et EXIT
            start_color = WHITE if self.selected_option == "START" else GRAY
            exit_color = WHITE if self.selected_option == "EXIT" else GRAY

            start_text = self.font_option.render("START", True, start_color)
            exit_text = self.font_option.render("EXIT", True, exit_color)

            self.screen.blit(start_text, (self.screen.get_width() // 2 - start_text.get_width() // 2, 250))
            self.screen.blit(exit_text, (self.screen.get_width() // 2 - exit_text.get_width() // 2, 350))

            # Dessine un contour autour de l'option sélectionnée
            if self.selected_option == "START":
                pygame.draw.rect(self.screen, WHITE, (self.screen.get_width() // 2 - 100, 240, 200, 50), 2)
            elif self.selected_option == "EXIT":
                pygame.draw.rect(self.screen, WHITE, (self.screen.get_width() // 2 - 100, 340, 200, 50), 2)

            pygame.display.flip()

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key in [pygame.K_UP, pygame.K_DOWN]:
                        self.selected_option = "EXIT" if self.selected_option == "START" else "START"

                    if event.key == pygame.K_RETURN:
                        if self.selected_option == "START":
                            pygame.mixer.music.stop()  # Arrêter la musique avant de lancer le jeu
                            return True  # Lancer le jeu
                        elif self.selected_option == "EXIT":
                            pygame.quit()
                            sys.exit()

            clock.tick(60)


def main():
    pygame.init()

    # Ouvrir la fenêtre en plein écran
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption("Draconic Generations")

    menu = Menu(screen)
    menu.show_menu()


if __name__ == "__main__":
    main()
