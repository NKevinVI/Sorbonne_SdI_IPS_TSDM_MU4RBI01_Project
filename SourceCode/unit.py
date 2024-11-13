import pygame
import random

# Constantes
GRID_SIZE = 5
CELL_SIZE = 128 # Default
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

WINDOW = pygame.display.set_mode((CELL_SIZE, CELL_SIZE))


class Unit:
    """
    Classe pour représenter une unité.

    ...
    Attributs
    ---------
    x : int
        La position x de l'unité sur la grille.
    y : int
        La position y de l'unité sur la grille.
    health : int
        La santé de l'unité.
    attack_power : int
        La puissance d'attaque de l'unité.
    team : str
        L'équipe de l'unité ('good' ou 'evil').
    is_selected : bool
        Si l'unité est sélectionnée ou non.

    Méthodes
    --------
    move(dx, dy)
        Déplace l'unité de dx, dy.
    attack(target)
        Attaque une unité cible.
    draw(screen)
        Dessine l'unité sur la grille.
    """

    def __init__(self, x, y, team, hierarchy):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.

        Paramètres
        ----------
        x : int
            La position x de l'unité sur la grille.
        y : int
            La position y de l'unité sur la grille.
        health : int
            La santé de l'unité.
        attack_power : int
            La puissance d'attaque de l'unité.
        team : str
            L'équipe de l'unité ('good' ou 'evil').
        hierarchy: str
            Il s'agit du type de l'unité.
                - "royal" => roi ou reine
                - "soldier" => wyverne ou gargouille
                - "pauper" => larve ou lindwurm
        """
        self.x = x
        self.y = y
        self.hierarchy = hierarchy
        self.team = team
        self.is_selected = False
        match self.hierarchy:
            case "royal":
                self.health = 180
                self.attack_power = 32
                self.resistance = 26
                self.speed = 1
            case "soldier":
                self.health = 32
                self.attack_power = 16
                self.resistance = 12
                self.speed = 7
            case "pauper":
                self.health = 60
                self.attack_power = 6
                self.resistance = 0
                self.speed = 3

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy

    def attack(self, target):
        """Attaque une unité cible."""
        if abs(self.x - target.x) <= 1 and abs(self.y - target.y) <= 1:
            if target.resistance <= self.attack_power:
                target.health -= self.attack_power - target.resistance
                if target.health < 0:
                    target.health = 0

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        if self.team == "good":
            color = GREEN
            match self.hierarchy:
                case "royal":
                    appearance = pygame.image.load("Textures/DragonQueen_Sketch.png").convert_alpha()
                case "soldier":
                    appearance = pygame.image.load("Textures/Amphiptere_Sketch.png").convert_alpha()
                case "pauper":
                    appearance = pygame.image.load("Textures/Lindwurm_Sketch.png").convert_alpha()
        elif self.team == "evil":
            color = RED
            match self.hierarchy:
                case "royal":
                    appearance = pygame.image.load("Textures/DracolichKing_Sketch.png").convert_alpha()
                case "soldier":
                    appearance = pygame.image.load("Textures/Gargouille_Sketch.png").convert_alpha()
                case "pauper":
                    appearance = pygame.image.load("Textures/Larva_Sketch.png").convert_alpha()
        else:
            raise ValueError("No other alignment yet!")
        appearance = pygame.transform.scale(appearance, (CELL_SIZE, CELL_SIZE))
        WINDOW.blit(appearance, (self.x * CELL_SIZE, self.y * CELL_SIZE))
        if self.is_selected:
            pygame.draw.rect(WINDOW, BLUE, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2*CELL_SIZE//CELL_SIZE)
