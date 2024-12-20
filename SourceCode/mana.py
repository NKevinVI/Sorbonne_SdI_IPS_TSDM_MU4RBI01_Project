import pygame
from abc import ABC, abstractmethod
import random
import os
import sys
import numpy as np

from var import *
from game import *
from unit import *
from menu import *
from VictoryDisplay import *


class Mana:
    def __init__(self, x, y):
        # Définie une source de mana à la position (x, y).
        self.x = x
        self.y = y
        self.here = True # La source est-elle encore viable? (Équivalent de is_alive.)
        self.rect = pygame.Rect(self.x * CELL_SIZE[0], self.y * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0])   #représente la position et la taille de la source

    def absorbed(self, owner):
        # Améliore la force d'attaque de celui qui l'a ramassé.
        self.here = False   # signifie que la source mana a été ramassé par une unité
        owner.attack_power += 4  #dans ce cas, l'unité qui l'a absorbé voit sa puissance augmenter de 4

    def draw(self, screen):
        # Imprime le mana sur la grille du jeu.
        if self.here:  #si la source est toujours présente, alors le code ci-dessous permet de représenter cette source
            pygame.draw.rect(WINDOW, CYAN, (self.x * CELL_SIZE[0] + int(2 * CELL_SIZE[0] / 5), self.y * CELL_SIZE[0] + int(2 * CELL_SIZE[0] / 5), int(CELL_SIZE[0] / 5), int(CELL_SIZE[0] / 5)))
