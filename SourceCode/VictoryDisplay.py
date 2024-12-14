import pygame
import random
import os
import sys
import numpy as np

from var import *
from game import *
from unit import *
from menu import *
from mana import *


class VictoryDisplay:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)  # Police par défaut avec une taille de 74
        self.font_title = pygame.font.Font(None, 80)  # Police pour le titre
        self.font_option = pygame.font.Font(None, 50)  # Police pour les options

    def play_music(self, music_file):
        """Joue une musique de victoire."""
        pygame.mixer.music.load(music_file)  # Charge le fichier audio
        pygame.mixer.music.play(-1)  # Joue la musique en boucle (-1 pour boucle, 0 pour une seule fois)
        pygame.mixer.music.set_volume(VOLUME)

    def show_good_won(self):
        """Affiche 'Les Dragons de Lumière ont vaincu!' en vert avec de la musique."""
        self.play_music("../Assets/good.mp3")
        self.screen.fill(BLACK)
        message = ["Les Dragons de Lumière ont vaincu!"]
        y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
        for line in message:
            font = pygame.font.Font(None, 50)
            text = font.render(line, True, GREEN)
            self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
            y += 50
        pygame.display.flip()
        button_selected = False
        show = True
        while show:
            self.screen.fill(BLACK)
            message = ["Les Dragons de Lumière ont vaincu!"]
            y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
            for line in message:
                font = pygame.font.Font(None, 50)
                text = font.render(line, True, GREEN)
                self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
                y += 50
            # Restart button.
            resButton_col = GREY if not(button_selected) else WHITE
            resButton_text = self.font_option.render("L'Enfer refera-t-il surface?", True, resButton_col)
            resButton_rect = pygame.Rect(WIDTH[0] // 2 - resButton_text.get_width() // 2, HEIGHT[0] // 2, resButton_text.get_width(), 50)
            self.screen.blit(resButton_text, (WIDTH[0] // 2 - resButton_text.get_width() // 2, HEIGHT[0] // 2 + 10))
            pygame.draw.rect(self.screen, WHITE, (WIDTH[0] // 2 - 225, HEIGHT[0] // 2, 450, 50), 2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                click_pos = pygame.mouse.get_pos()
                if resButton_rect.collidepoint(click_pos):
                    button_selected = True
                else:
                    button_selected = False
                if event.type == pygame.MOUSEBUTTONDOWN and button_selected:
                    show = False
                if event.type == pygame.VIDEORESIZE:
                    CELL_SIZE[0] = min(self.screen.get_width() // GRID_SIZE, self.screen.get_height() // GRID_SIZE)
                    WIDTH[0] = GRID_SIZE * CELL_SIZE[0]
                    HEIGHT[0] = WIDTH[0]
                    y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
                if event.type == pygame.KEYDOWN:
                    pygame.display.flip()
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)


    def show_evil_won(self):
        """Affiche 'Les Dragones de l'Ombre ont vaincu!' en vert avec de la musique."""
        self.play_music("../Assets/evil.mp3")
        self.screen.fill(BLACK)
        message = ["Les Dragones de l'Ombre ont vaincu!"]
        y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
        for line in message:
            font = pygame.font.Font(None, 50)
            text = font.render(line, True, RED)
            self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
            y += 50
        pygame.display.flip()
        button_selected = False
        show = True
        while show:
            self.screen.fill(BLACK)
            message = ["Les Dragons de l'Ombre ont vaincu!"]
            y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
            for line in message:
                font = pygame.font.Font(None, 50)
                text = font.render(line, True, RED)
                self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
                y += 50
            # Restart button.
            resButton_col = GREY if not(button_selected) else WHITE
            resButton_text = self.font_option.render("La Lumière refera-t-elle surface?", True, resButton_col)
            resButton_rect = pygame.Rect(WIDTH[0] // 2 - resButton_text.get_width() // 2, HEIGHT[0] // 2, resButton_text.get_width(), 50)
            self.screen.blit(resButton_text, (WIDTH[0] // 2 - resButton_text.get_width() // 2, HEIGHT[0] // 2 + 10))
            pygame.draw.rect(self.screen, WHITE, (WIDTH[0] // 2 - 270, HEIGHT[0] // 2, 540, 50), 2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                click_pos = pygame.mouse.get_pos()
                if resButton_rect.collidepoint(click_pos):
                    button_selected = True
                else:
                    button_selected = False
                if event.type == pygame.MOUSEBUTTONDOWN and button_selected:
                    show = False
                if event.type == pygame.VIDEORESIZE:
                    CELL_SIZE[0] = min(self.screen.get_width() // GRID_SIZE, self.screen.get_height() // GRID_SIZE)
                    WIDTH[0] = GRID_SIZE * CELL_SIZE[0]
                    HEIGHT[0] = WIDTH[0]
                    y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
                if event.type == pygame.KEYDOWN:
                    pygame.display.flip()
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

    def show_tie(self):
        """Affiche le cas où aucun des joueurs ne gagnent."""
        self.play_music("../Assets/tie.mp3")
        self.screen.fill(BLACK)
        message = ["L'Espèce Draconique est éteinte"]
        y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
        for line in message:
            font = pygame.font.Font(None, 50)
            text = font.render(line, True, WHITE)
            self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
            y += 50
        pygame.display.flip()
        button_selected = False
        show = True
        while show:
            self.screen.fill(BLACK)
            message = ["L'Espèce Draconique est éteinte"]
            y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
            for line in message:
                font = pygame.font.Font(None, 50)
                text = font.render(line, True, WHITE)
                self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
                y += 50
            # Restart button.
            resButton_col = GREY if not(button_selected) else WHITE
            resButton_text = self.font_option.render("Une nouvelle génération?", True, resButton_col)
            resButton_rect = pygame.Rect(WIDTH[0] // 2 - resButton_text.get_width() // 2, HEIGHT[0] // 2, resButton_text.get_width(), 50)
            self.screen.blit(resButton_text, (WIDTH[0] // 2 - resButton_text.get_width() // 2, HEIGHT[0] // 2 + 10))
            pygame.draw.rect(self.screen, WHITE, (WIDTH[0] // 2 - 270, HEIGHT[0] // 2, 540, 50), 2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                click_pos = pygame.mouse.get_pos()
                if resButton_rect.collidepoint(click_pos):
                    button_selected = True
                else:
                    button_selected = False
                if event.type == pygame.MOUSEBUTTONDOWN and button_selected:
                    show = False
                if event.type == pygame.VIDEORESIZE:
                    CELL_SIZE[0] = min(self.screen.get_width() // GRID_SIZE, self.screen.get_height() // GRID_SIZE)
                    WIDTH[0] = GRID_SIZE * CELL_SIZE[0]
                    HEIGHT[0] = WIDTH[0]
                    y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
                if event.type == pygame.KEYDOWN:
                    pygame.display.flip()
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

    def show_no_war(self):
        """Affiche le cas où aucun des joueurs ne gagnent, mais des unités sont encore viables."""
        self.play_music("../Assets/menu_music.mp3")
        self.screen.fill(BLACK)
        message = ["Paix sur les Royaumes!", "", "(Pas de mort depuis trop longtemps.)"]
        y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
        for line in message:
            font = pygame.font.Font(None, 50)
            text = font.render(line, True, WHITE if line != "(Pas de mort depuis trop longtemps.)" else GREY)
            self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
            y += 50
        pygame.display.flip()
        button_selected = False
        show = True
        while show:
            self.screen.fill(BLACK)
            message = ["Paix sur les Royaumes!", "", "(Pas de mort depuis trop longtemps.)"]
            y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
            for line in message:
                font = pygame.font.Font(None, 50)
                text = font.render(line, True, WHITE if line != "(Pas de mort depuis trop longtemps.)" else GREY)
                self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
                y += 50
            # Restart button.
            resButton_col = GREY if not(button_selected) else WHITE
            resButton_text = self.font_option.render("Y aura-t-il une nouvelle querelle?", True, resButton_col)
            resButton_rect = pygame.Rect(WIDTH[0] // 2 - resButton_text.get_width() // 2, HEIGHT[0] // 2, resButton_text.get_width(), 50)
            self.screen.blit(resButton_text, (WIDTH[0] // 2 - resButton_text.get_width() // 2, HEIGHT[0] // 2 + 10))
            pygame.draw.rect(self.screen, WHITE, (WIDTH[0] // 2 - 275, HEIGHT[0] // 2, 550, 50), 2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                click_pos = pygame.mouse.get_pos()
                if resButton_rect.collidepoint(click_pos):
                    button_selected = True
                else:
                    button_selected = False
                if event.type == pygame.MOUSEBUTTONDOWN and button_selected:
                    show = False
                if event.type == pygame.VIDEORESIZE:
                    CELL_SIZE[0] = min(self.screen.get_width() // GRID_SIZE, self.screen.get_height() // GRID_SIZE)
                    WIDTH[0] = GRID_SIZE * CELL_SIZE[0]
                    HEIGHT[0] = WIDTH[0]
                    y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
                if event.type == pygame.KEYDOWN:
                    pygame.display.flip()
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)

    def show_easter(self):
        """
            Affiche l'Easter Egg (les deux joueurs gagnent simultanément).
        """
        self.play_music("../Assets/love.mp3")
        self.screen.fill(BLACK)
        message = ["Paix durable entre les Royaumes!","La Reine Dragon et le Roi Dragon se sont liés!","","(Easter Egg)"]
        y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
        for line in message:
            font = pygame.font.Font(None, 50)
            text = font.render(line, True, WHITE if line != "(Easter Egg)" else GREY)
            self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
            y += 50
        pygame.display.flip()
        button_selected = False
        show = True
        while show:
            self.screen.fill(BLACK)
            message = ["Paix durable entre les Royaumes!","La Reine Dragon et le Roi Dragon se sont liés!","","(Easter Egg)"]
            y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
            for line in message:
                font = pygame.font.Font(None, 50)
                text = font.render(line, True, WHITE if line != "(Easter Egg)" else GREY)
                self.screen.blit(text, (WIDTH[0] // 2 - text.get_width() // 2, y))
                y += 50
            # Restart button.
            resButton_col = GREY if not(button_selected) else WHITE
            resButton_text = self.font_option.render("Auront-ils des héritiers?", True, resButton_col)
            resButton_rect = pygame.Rect(WIDTH[0] // 2 - resButton_text.get_width() // 2, HEIGHT[0] // 2, resButton_text.get_width(), 50)
            self.screen.blit(resButton_text, (WIDTH[0] // 2 - resButton_text.get_width() // 2, HEIGHT[0] // 2 + 10))
            pygame.draw.rect(self.screen, WHITE, (WIDTH[0] // 2 - 225, HEIGHT[0] // 2, 450, 50), 2)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                click_pos = pygame.mouse.get_pos()
                if resButton_rect.collidepoint(click_pos):
                    button_selected = True
                else:
                    button_selected = False
                if event.type == pygame.MOUSEBUTTONDOWN and button_selected:
                    show = False
                if event.type == pygame.VIDEORESIZE:
                    CELL_SIZE[0] = min(self.screen.get_width() // GRID_SIZE, self.screen.get_height() // GRID_SIZE)
                    WIDTH[0] = GRID_SIZE * CELL_SIZE[0]
                    HEIGHT[0] = WIDTH[0]
                    y = HEIGHT[0] // 2 - 200 # Hauteur initiale du message.
                    pygame.display.flip()
                if event.type == pygame.KEYDOWN:
                    pygame.display.flip()
            pygame.display.flip()
            pygame.time.Clock().tick(FPS)
