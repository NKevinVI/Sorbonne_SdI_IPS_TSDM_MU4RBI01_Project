import pygame
import random
import os
import sys
import numpy as np

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
        self.play_music("../Assets/good.mp3")
        pygame.mixer.music.play(-1)  # Lecture en boucle
        self.screen.fill(BLACK)
        message = ["Les Dragons de Lumière ont vaincu!"]
        y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
        for line in message:
            font = pygame.font.Font(None, 50)
            text = font.render(line, True, GREEN)
            self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
            y += 50
            pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_music()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    CELL_SIZE[0] = min(self.screen.get_width() // GRID_SIZE, self.screen.get_height() // GRID_SIZE)
                    WIDTH[0] = GRID_SIZE * CELL_SIZE[0]
                    HEIGHT[0] = WIDTH[0]
                    y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
                    for line in message:
                        font = pygame.font.Font(None, 50)
                        text = font.render(line, True, GREEN)
                        self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
                        y += 50
                    pygame.display.flip()
                if event.type == pygame.KEYDOWN:
                    pygame.display.flip()
            pygame.time.Clock().tick(FPS)

    def show_evil_won(self):
        """Affiche 'Les Dragons de l'Ombre ont vaincu!' en rouge avec de la musique."""
        self.play_music("../Assets/evil.mp3")
        pygame.mixer.music.play(-1)  # Lecture en boucle
        self.screen.fill(BLACK)
        message = ["Les Dragons de l'Ombre ont vaincu!"]
        y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
        for line in message:
            font = pygame.font.Font(None, 50)
            text = font.render(line, True, RED)
            self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
            y += 50
            pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_music()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    CELL_SIZE[0] = min(self.screen.get_width() // GRID_SIZE, self.screen.get_height() // GRID_SIZE)
                    WIDTH[0] = GRID_SIZE * CELL_SIZE[0]
                    HEIGHT[0] = WIDTH[0]
                    y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
                    for line in message:
                        font = pygame.font.Font(None, 50)
                        text = font.render(line, True, RED)
                        self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
                        y += 50
                    pygame.display.flip()
                if event.type == pygame.KEYDOWN:
                    pygame.display.flip()
            pygame.time.Clock().tick(FPS)

    def show_tie(self):
        """Affiche 'Les Dragons de l'Ombre ont vaincu!' en rouge avec de la musique."""
        self.play_music("../Assets/tie.mp3")
        pygame.mixer.music.play(-1)  # Lecture en boucle
        self.screen.fill(BLACK)
        message = ["L'Espèce Draconique est éteinte!"]
        y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
        for line in message:
            font = pygame.font.Font(None, 50)
            text = font.render(line, True, WHITE)
            self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
            y += 50
            pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_music()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    CELL_SIZE[0] = min(self.screen.get_width() // GRID_SIZE, self.screen.get_height() // GRID_SIZE)
                    WIDTH[0] = GRID_SIZE * CELL_SIZE[0]
                    HEIGHT[0] = WIDTH[0]
                    y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
                    for line in message:
                        font = pygame.font.Font(None, 50)
                        text = font.render(line, True, WHITE)
                        self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
                        y += 50
                    pygame.display.flip()
                if event.type == pygame.KEYDOWN:
                    pygame.display.flip()
            pygame.time.Clock().tick(FPS)

    def show_easter(self):
        """
            Affiche l'Easter Egg (les deux joueurs gagnent simultanément).
        """
        self.play_music("../Assets/love.mp3")
        pygame.mixer.music.play(-1)  # Lecture en boucle
        self.screen.fill(BLACK)
        message = ["Paix durable entre les Royaumes!","La Reine Dragon et le Roi Dragon se sont liés!","","(Easter Egg)"]
        y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
        for line in message:
            font = pygame.font.Font(None, 50)
            text = font.render(line, True, WHITE if line != "(Easter Egg)" else (100,100,100))
            self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
            y += 50
            pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.stop_music()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.VIDEORESIZE:
                    CELL_SIZE[0] = min(self.screen.get_width() // GRID_SIZE, self.screen.get_height() // GRID_SIZE)
                    WIDTH[0] = GRID_SIZE * CELL_SIZE[0]
                    HEIGHT[0] = WIDTH[0]
                    y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
                    for line in message:
                        font = pygame.font.Font(None, 50)
                        text = font.render(line, True, WHITE if line != "(Easter Egg)" else GREY)
                        self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
                        y += 50
                    pygame.display.flip()
                if event.type == pygame.KEYDOWN:
                    pygame.display.flip()
            pygame.time.Clock().tick(FPS)
