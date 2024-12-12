import pygame
import random
import os
import sys
import numpy as np

from var import *
from game import *
from unit import *
from VictoryDisplay import *
from mana import *


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
            path = os.path.join("..", "Assets", "background.jpg")  # Chemin attendu
            self.background = pygame.image.load(path)
            self.background = pygame.transform.scale(self.background, (WIDTH[0], HEIGHT[0]))
        except FileNotFoundError:
            print(f"Erreur : L'image 'background.jpg' est introuvable.")
            print(f"Chemin absolu recherché : {os.path.abspath(path)}")
            sys.exit()  #quitte si l'image n'est pas trouvée

        # Charger la musique de fond
        try:
            pygame.mixer.music.load(os.path.join("..", "Assets", "menu_music.mp3"))
            pygame.mixer.music.play(-1)  # Lecture en boucle
            pygame.mixer.music.set_volume(VOLUME)
        except FileNotFoundError:
            print("Erreur : La musique 'menu_music.mp3' est introuvable.")
            sys.exit()

    def display(self):
        """Affiche le menu."""

        # Met à jour les dimensions de la fenêtre.
        CELL_SIZE[0] = min(self.screen.get_width() // GRID_SIZE, self.screen.get_height() // GRID_SIZE)
        WIDTH[0] = GRID_SIZE * CELL_SIZE[0]
        HEIGHT[0] = WIDTH[0]

        # Rafraîchit l'écran
        pygame.display.flip()

        while True:
            # Afficher l'image de fond
            self.screen.blit(self.background, (0, 0))

            # Affiche le titre
            title_text = self.font_title.render("Draconic Generations", True, YELLOW)
            self.screen.blit(title_text, (WIDTH[0] // 2 - title_text.get_width() // 2, 100))

            # Affiche les options START et EXIT
            start_color = WHITE if self.selected_option == "START" else BLACK
            exit_color = WHITE if self.selected_option == "EXIT" else BLACK

            start_text = self.font_option.render("START", True, start_color)
            exit_text = self.font_option.render("EXIT", True, exit_color)

            start_rect = pygame.Rect(WIDTH[0] // 2 - 100, 440, 200, 50)
            exit_rect = pygame.Rect(WIDTH[0] // 2 - 100, 540, 200, 50)

            self.screen.blit(start_text, (WIDTH[0] // 2 - start_text.get_width() // 2, 450))
            self.screen.blit(exit_text, (WIDTH[0] // 2 - exit_text.get_width() // 2, 550))

            # Dessine un contour autour de l'option sélectionnée
            if self.selected_option == "START":
                pygame.draw.rect(self.screen, WHITE, (WIDTH[0] // 2 - 100, 440, 200, 50), 2)
            elif self.selected_option == "EXIT":
                pygame.draw.rect(self.screen, WHITE, (WIDTH[0] // 2 - 100, 540, 200, 50), 2)

            self.background = pygame.transform.scale(self.background, (WIDTH[0], HEIGHT[0]))
            pygame.display.flip()

            # Gestion des événements
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    CELL_SIZE[0] = min(self.screen.get_width() // GRID_SIZE, self.screen.get_height() // GRID_SIZE)
                    WIDTH[0] = GRID_SIZE * CELL_SIZE[0]
                    HEIGHT[0] = WIDTH[0]
                    self.background = pygame.transform.scale(self.background, (WIDTH[0], HEIGHT[0]))
                    pygame.display.flip()

                if event.type == pygame.KEYDOWN: # On met à jour l'onglet.
                    CELL_SIZE[0] = min(self.screen.get_width() // GRID_SIZE, self.screen.get_height() // GRID_SIZE)
                    WIDTH[0] = GRID_SIZE * CELL_SIZE[0]
                    HEIGHT[0] = WIDTH[0]
                    pygame.display.flip()

                click_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(click_pos):
                    self.selected_option = "START"
                elif exit_rect.collidepoint(click_pos):
                    self.selected_option = "EXIT"

                if event.type == pygame.MOUSEBUTTONDOWN:
                    CELL_SIZE[0] = min(self.screen.get_width() // GRID_SIZE, self.screen.get_height() // GRID_SIZE)
                    WIDTH[0] = GRID_SIZE * CELL_SIZE[0]
                    HEIGHT[0] = WIDTH[0]
                    pygame.display.flip()

                    if start_rect.collidepoint(click_pos):
                        pygame.mixer.music.stop()  # Arrêter la musique avant de lancer le jeu
                        return True  # Lancer le jeu
                    elif exit_rect.collidepoint(click_pos):
                        pygame.quit()
                        sys.exit()
            pygame.time.Clock().tick(FPS)
