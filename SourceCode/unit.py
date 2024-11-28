import pygame
import random

# Constantes
GRID_SIZE = 7
CELL_SIZE = 128 # Default
WIDTH = GRID_SIZE * CELL_SIZE
HEIGHT = GRID_SIZE * CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)

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

    def __init__(self, x, y, team):
        """
        Construit une unité avec une position, une santé, une puissance d'attaque et une équipe.
        """
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        self.team = team
        self.is_selected = False
        self.move_count = 0
        self.is_alive = True

    def move(self, dx, dy):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy
        self.rect = pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

    def attack_simple(self, target):
        """Attaque une unité cible."""
        target.health -= self.attack_power - target.resistance
        if target.health <= 0:
            target.health = 0
            target.is_alive = False

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        pass

class Royal(Unit): # L'unité royale, bonne ou mauvaise.
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.hierarchy = "royal"
        self.health = 60
        self.attack_power = 32
        self.resistance = 16
        self.speed = 1

    def draw(self, screen):
        if self.is_alive:
            if self.team == "good":
                color = BLUE
                appearance = pygame.image.load("../Textures/DragonQueen_Sketch.png").convert_alpha()
            elif self.team == "evil":
                color = RED
                appearance = pygame.image.load("../Textures/DracolichKing_Sketch.png").convert_alpha()
            else:
                raise ValueError("No other alignment yet!")
            appearance = pygame.transform.scale(appearance, (CELL_SIZE, CELL_SIZE))
            WINDOW.blit(appearance, (self.x * CELL_SIZE, self.y * CELL_SIZE))

            # Affiche self.health à l'écran.
            pygame.draw.rect(WINDOW, RED, (int(CELL_SIZE * (self.x + 11/12)), int(self.y * CELL_SIZE), int(CELL_SIZE * 1/12), int(CELL_SIZE)))
            pygame.draw.rect(WINDOW, GREEN, (int(CELL_SIZE * (self.x + 11/12)), int(CELL_SIZE * (self.y + 1 - self.health / 60)), int(CELL_SIZE * 1/12), int(CELL_SIZE * self.health / 60)))

            if self.is_selected:
                pygame.draw.rect(WINDOW, BLUE, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)

class Soldier(Unit): # L'unité royale, bonne ou mauvaise.
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.hierarchy = "royal"
        self.health = 36
        self.attack_power = 23
        self.resistance = 13
        self.speed = 4

    def draw(self, screen):
        if self.is_alive:
            if self.team == "good":
                color = BLUE
                appearance = pygame.image.load("../Textures/Amphiptere_Sketch.png").convert_alpha()
            elif self.team == "evil":
                color = RED
                appearance = pygame.image.load("../Textures/Gargouille_Sketch.png").convert_alpha()
            else:
                raise ValueError("No other alignment yet!")
            appearance = pygame.transform.scale(appearance, (CELL_SIZE, CELL_SIZE))
            WINDOW.blit(appearance, (self.x * CELL_SIZE, self.y * CELL_SIZE))

            # Affiche self.health à l'écran.
            pygame.draw.rect(WINDOW, RED, (int(CELL_SIZE * (self.x + 11/12)), int(self.y * CELL_SIZE), int(CELL_SIZE * 1/12), int(CELL_SIZE)))
            pygame.draw.rect(WINDOW, GREEN, (int(CELL_SIZE * (self.x + 11/12)), int(CELL_SIZE * (self.y + 1 - self.health / 60)), int(CELL_SIZE * 1/12), int(CELL_SIZE * self.health / 60)))

            if self.is_selected:
                pygame.draw.rect(WINDOW, BLUE, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)

class Pauper(Unit): # L'unité royale, bonne ou mauvaise.
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.hierarchy = "royal"
        self.health = 23
        self.attack_power = 16
        self.resistance = 6
        self.speed = 2

    def draw(self, screen):
        if self.is_alive:
            if self.team == "good":
                color = BLUE
                appearance = pygame.image.load("../Textures/Lindwurm_Sketch.png").convert_alpha()
            elif self.team == "evil":
                color = RED
                appearance = pygame.image.load("../Textures/Larva_Sketch.png").convert_alpha()
            else:
                raise ValueError("No other alignment yet!")
            appearance = pygame.transform.scale(appearance, (CELL_SIZE, CELL_SIZE))
            WINDOW.blit(appearance, (self.x * CELL_SIZE, self.y * CELL_SIZE))

            # Affiche self.health à l'écran.
            pygame.draw.rect(WINDOW, RED, (int(CELL_SIZE * (self.x + 11/12)), int(self.y * CELL_SIZE), int(CELL_SIZE * 1/12), int(CELL_SIZE)))
            pygame.draw.rect(WINDOW, GREEN, (int(CELL_SIZE * (self.x + 11/12)), int(CELL_SIZE * (self.y + 1 - self.health / 60)), int(CELL_SIZE * 1/12), int(CELL_SIZE * self.health / 60)))

            if self.is_selected:
                pygame.draw.rect(WINDOW, BLUE, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
