import pygame
from abc import ABC, abstractmethod
import random
import os
import sys
import numpy as np

# Constantes et valeurs par défaut.
BOARD = np.array([[-1,0,0,0,0,0,1],
                [0,0,1,0,-1,0,0],
                [-1,-1,0,0,0,1,1],
                [-1,-1,0,0,0,1,1],
                [-1,-1,0,0,0,1,1],
                [0,0,1,0,-1,0,0],
                [-1,0,0,0,0,0,1]]) # Le BOARD doit absolumant être un carré! Ou vous subirez mon courroux!
GRID_SIZE = len(BOARD)
CELL_SIZE = [128] # Default
WIDTH = [GRID_SIZE * CELL_SIZE[0]]
HEIGHT = [WIDTH[0]] # On est forcément dans un carré!
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
DARK_RED = (100, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 100, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
GREY = (100, 100, 100)
VOLUME = 0.25 # Volume sonore des musiques.

NB_TURN_TIE = 60 # Nombre de tours (par joueur) avant une partie nulle, si pas de mort.

WINDOW = pygame.display.set_mode((CELL_SIZE[0], CELL_SIZE[0]))
