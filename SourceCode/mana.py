import pygame
import random

from unit import *


class Mana:
    def __init__(self, x, y):
        # Définie une source de mana à la position (x, y).
        self.x = x
        self.y = y
        self.here = True # La source est-elle encore viable? (Équivalent de is_alive.)
        self.rect = pygame.Rect(self.x * CELL_SIZE[0], self.y * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0])

    def draw(self, screen):
        # Imprime le mana sur la grille du jeu.
        if self.here:
            pygame.draw.rect(WINDOW, CYAN, (self.x * CELL_SIZE[0] + int(2 * CELL_SIZE[0] / 5), self.y * CELL_SIZE[0] + int(2 * CELL_SIZE[0] / 5), int(CELL_SIZE[0] / 5), int(CELL_SIZE[0] / 5)))
