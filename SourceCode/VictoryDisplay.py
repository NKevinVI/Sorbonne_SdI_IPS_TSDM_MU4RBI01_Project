import pygame
import random
import os
import sys

from unit import *

class VictoryDisplay:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)  # Police par défaut avec une taille de 74
        pygame.mixer.init()  # Initialisation du module audio

    def display_message(self, message, color):
        """Affiche un message centré sur l'écran."""
        self.screen.fill((0, 0, 0))  # Efface l'écran avec une couleur noire
        text = self.font.render(message, True, color)  # Rend le texte
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)  # Dessine le texte
        pygame.display.flip()  # Met à jour l'écran

    def play_music(self, music_file):
        """Joue une musique de victoire."""
        pygame.mixer.music.load(music_file)  # Charge le fichier audio
        pygame.mixer.music.play(-1)  # Joue la musique en boucle (-1 pour boucle, 0 pour une seule fois)

    def stop_music(self):
        """Arrête la musique."""
        pygame.mixer.music.stop()

    def show_good_won(self):
        """Affiche 'Les Dragons de Lumière ont vaincu!' en vert avec de la musique."""
        self.play_music("you_win.mp3")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_music()  # Arrête la musique avant de quitter
                    pygame.quit()
                    sys.exit()
            self.display_message("Les Dragons de Lumière ont vaincu!", GREEN)

    def show_evil_won(self):
        """Affiche 'Les Dragons de l'Ombre ont vaincu!' en rouge avec de la musique."""
        self.play_music("you_win.mp3")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_music()  # Arrête la musique avant de quitter
                    pygame.quit()
                    sys.exit()
            self.display_message("Les Dragons de l'Ombre ont vaincu!", RED)

    def show_tie(self):
        """Affiche 'Les Dragons de l'Ombre ont vaincu!' en rouge avec de la musique."""
        self.play_music("you_win.mp3")
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_music()  # Arrête la musique avant de quitter
                    pygame.quit()
                    sys.exit()
            self.display_message("Les Dragons sont éteints!", WHITE)
