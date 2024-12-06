import pygame
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

WINDOW = pygame.display.set_mode((CELL_SIZE[0], CELL_SIZE[0]))


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
        self.rect = pygame.Rect(self.x * CELL_SIZE[0], self.y * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0])
        self.team = team
        self.is_selected = False
        self.move_count = 0
        self.is_alive = True
        self.protected = False # L'unité est-elle protégée des attaques à distance?

    def move(self, dx, dy, game):
        """Déplace l'unité de dx, dy."""
        if 0 <= self.x + dx < GRID_SIZE and 0 <= self.y + dy < GRID_SIZE:
            self.x += dx
            self.y += dy
        self.rect = pygame.Rect(self.x * CELL_SIZE[0], self.y * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0])
        game.flip_display()

    def dmg(self, dmg):
        # Quand l'unité reçoit des dégâts.
        if dmg <= self.resistance:
            return
        else:
            self.health -= dmg - self.resistance
            if self.health <= 0:
                self.health = 0
                self.is_alive = False

    def attack_simple(self, evils, goods, Attaque, Deplacer, event, target, game):
        """Attaque une unité cible adjacente à l'unité principale."""
        if not(Deplacer) and event.key == pygame.K_SPACE and target != [self.x, self.y] and not(Attaque):
            for unit in evils + goods:
                if unit.x == target[0] and unit.y == target[1]:
                    target = unit
                    break
            if isinstance(target, Unit):
                target.dmg(self.attack_power)
                Attaque = True # L'unité a attaqué.
                game.flip_display()

        return Attaque

    def attack_show(self, target, Attaque, Deplacer, event):
        """
        Indique ce qu'on s'apprête à attaquer (case adjacente).

        Attaque -> A-t-on déjà attaqué?
        Deplacer -> Nous sommes-nous déjà déplacés?
        game -> L'instance gérant le jeu entier.
        event -> pygame event.
        """
        # Attaque simple:
        if not(Deplacer) and event.key == pygame.K_z and not(Attaque):
            target = [self.x, self.y - 1]
            pygame.draw.rect(WINDOW, RED, (target[0] * CELL_SIZE[0], target[1] * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)
        elif not(Deplacer) and event.key == pygame.K_q and not(Attaque):
            target = [self.x - 1, self.y]
            pygame.draw.rect(WINDOW, RED, (target[0] * CELL_SIZE[0], target[1] * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)
        elif not(Deplacer) and event.key == pygame.K_s and not(Attaque):
            target = [self.x, self.y + 1]
            pygame.draw.rect(WINDOW, RED, (target[0] * CELL_SIZE[0], target[1] * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)
        elif not(Deplacer) and event.key == pygame.K_d and not(Attaque):
            target = [self.x + 1, self.y]
            pygame.draw.rect(WINDOW, RED, (target[0] * CELL_SIZE[0], target[1] * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)

        pygame.display.flip()

        return target

    def draw(self, screen):
        """Affiche l'unité sur l'écran."""
        pass

class Royal(Unit): # L'unité royale, bonne ou mauvaise.
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.health = 60
        self.attack_power = 32
        self.resistance = 16
        self.speed = 1

    def attack_berserk(self, evils, goods, Attaque, Deplacer, event, target, game):
        # Attaque une unité target en mode berserk.
        if not(Deplacer) and event.key == pygame.K_x and target != [self.x, self.y] and not(Attaque):
            for unit in evils + goods:
                if unit.x == target[0] and unit.y == target[1]:
                    target = unit
                    break
            if isinstance(target, Unit):
                target.dmg(int(1.5 * self.attack_power) + target.resistance)
                self.dmg(int(0.5 * self.attack_power + 16))
                Attaque = True # L'unité a attaqué.
                game.flip_display()

        return Attaque

    def draw(self, screen):
        self.rect = pygame.Rect(self.x * CELL_SIZE[0], self.y * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0])
        if self.is_alive:
            if self.team == "good":
                color = BLUE
                appearance = pygame.image.load("../Textures/DragonQueen_Sketch.png").convert_alpha()
            elif self.team == "evil":
                color = RED
                appearance = pygame.image.load("../Textures/DracolichKing_Sketch.png").convert_alpha()
            else:
                raise ValueError("No other alignment yet!")
            appearance = pygame.transform.scale(appearance, (CELL_SIZE[0], CELL_SIZE[0]))
            WINDOW.blit(appearance, (self.x * CELL_SIZE[0], self.y * CELL_SIZE[0]))

            # Affiche self.health à l'écran.
            pygame.draw.rect(WINDOW, RED, (int(CELL_SIZE[0] * (self.x + 11/12)), int(self.y * CELL_SIZE[0]), int(CELL_SIZE[0] * 1/12), int(CELL_SIZE[0])))
            pygame.draw.rect(WINDOW, GREEN, (int(CELL_SIZE[0] * (self.x + 11/12)), int(CELL_SIZE[0] * (self.y + 1 - self.health / 60)), int(CELL_SIZE[0] * 1/12), int(CELL_SIZE[0] * self.health / 60)))

            if self.is_selected:
                pygame.draw.rect(WINDOW, BLUE, (self.x * CELL_SIZE[0], self.y * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)

class Soldier(Unit): # Le soldat.
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.health = 36
        self.attack_power = 23
        self.resistance = 13
        self.speed = 4

    def attack_special(self, area, foe):
        """
        Attaque sur une surface area particulière.
        L'argument area est une liste [x,y], représentant une surface telle que:
        _ X _
        X O X
        _ X _
        avec le "O" étant aux coordonnées [x,y] et étant une zone touchée, le "X" une zone touchée, et "_" les zones non affectées.
        Le foe est un ennemi potentiel.
        """
        if not foe.protected: # Si le foe n'est pas sur une case qui le protège, il ne prend pas de dégât.
            if area[0] == 0:
                if area[1] == 0:
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint((area[0] + 1) * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], (area[1] + 1) * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                elif area[1] == int(HEIGHT[0]/GRID_SIZE) - 1:
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint((area[0] + 1) * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], (area[1] - 1) * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                else:
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint((area[0] + 1) * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], (area[1] + 1) * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], (area[1] - 1) * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
            elif area[0] == int(WIDTH[0]/GRID_SIZE) - 1:
                if area[1] == 0:
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint((area[0] - 1) * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], (area[1] + 1) * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                elif area[1] == int(HEIGHT[0]/GRID_SIZE) - 1:
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint((area[0] - 1) * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], (area[1] - 1) * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                else:
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint((area[0] - 1) * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], (area[1] + 1) * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], (area[1] - 1) * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
            else:
                if area[1] == 0:
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint((area[0] - 1) * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint((area[0] + 1) * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], (area[1] + 1) * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                elif area[1] == int(HEIGHT[0]/GRID_SIZE) - 1:
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint((area[0] - 1) * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint((area[0] + 1) * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], (area[1] - 1) * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                else:
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint((area[0] - 1) * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint((area[0] + 1) * CELL_SIZE[0], area[1] * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], (area[1] + 1) * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)
                    if foe.rect.collidepoint(area[0] * CELL_SIZE[0], (area[1] - 1) * CELL_SIZE[0]):
                        foe.dmg(self.attack_power - 4)

    def draw(self, screen):
        self.rect = pygame.Rect(self.x * CELL_SIZE[0], self.y * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0])
        if self.is_alive:
            if self.team == "good":
                color = BLUE
                appearance = pygame.image.load("../Textures/Amphiptere_Sketch.png").convert_alpha()
            elif self.team == "evil":
                color = RED
                appearance = pygame.image.load("../Textures/Gargouille_Sketch.png").convert_alpha()
            else:
                raise ValueError("No other alignment yet!")
            appearance = pygame.transform.scale(appearance, (CELL_SIZE[0], CELL_SIZE[0]))
            WINDOW.blit(appearance, (self.x * CELL_SIZE[0], self.y * CELL_SIZE[0]))

            # Affiche self.health à l'écran.
            pygame.draw.rect(WINDOW, RED, (int(CELL_SIZE[0] * (self.x + 11/12)), int(self.y * CELL_SIZE[0]), int(CELL_SIZE[0] * 1/12), int(CELL_SIZE[0])))
            pygame.draw.rect(WINDOW, GREEN, (int(CELL_SIZE[0] * (self.x + 11/12)), int(CELL_SIZE[0] * (self.y + 1 - self.health / 60)), int(CELL_SIZE[0] * 1/12), int(CELL_SIZE[0] * self.health / 60)))

            if self.is_selected:
                pygame.draw.rect(WINDOW, BLUE, (self.x * CELL_SIZE[0], self.y * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)

class Pauper(Unit): # Le bas peuple.
    def __init__(self, x, y, team):
        super().__init__(x, y, team)
        self.health = 23
        self.attack_power = 17
        self.resistance = 11
        self.speed = 2

    def heal(self, Attaque, Deplacer, event, game):
        # Action permettant de s'auto-régénérer.
        if not(Attaque) and not(Deplacer) and event.key == pygame.K_x and self.health < 23:
            self.health += int(self.attack_power / 2)
            if self.health >= 23:
                self.health = 23
            game.flip_display()
            Attaque = True
        return Attaque

    def attack_simple(self, evils, goods, Attaque, Deplacer, event, target, game):
        """Attaque une unité cible adjacente à l'unité principale."""
        if event.key == pygame.K_SPACE and target != [self.x, self.y] and not(Attaque):
            for unit in evils + goods:
                if unit.x == target[0] and unit.y == target[1]:
                    target = unit
                    break
            if isinstance(target, Unit):
                target.dmg(self.attack_power)
                Attaque = True # L'unité a attaqué.
                game.flip_display()

        return Attaque

    def attack_show(self, target, Attaque, Deplacer, event):
        """
        Indique ce qu'on s'apprête à attaquer (case adjacente).

        Attaque -> A-t-on déjà attaqué?
        Deplacer -> Nous sommes-nous déjà déplacés?
        game -> L'instance gérant le jeu entier.
        event -> pygame event.
        """
        # Attaque simple:
        if event.key == pygame.K_z and not(Attaque):
            target = [self.x, self.y - 1]
            pygame.draw.rect(WINDOW, RED, (target[0] * CELL_SIZE[0], target[1] * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)
        elif event.key == pygame.K_q and not(Attaque):
            target = [self.x - 1, self.y]
            pygame.draw.rect(WINDOW, RED, (target[0] * CELL_SIZE[0], target[1] * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)
        elif event.key == pygame.K_s and not(Attaque):
            target = [self.x, self.y + 1]
            pygame.draw.rect(WINDOW, RED, (target[0] * CELL_SIZE[0], target[1] * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)
        elif event.key == pygame.K_d and not(Attaque):
            target = [self.x + 1, self.y]
            pygame.draw.rect(WINDOW, RED, (target[0] * CELL_SIZE[0], target[1] * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)

        pygame.display.flip()

        return target

    def draw(self, screen):
        self.rect = pygame.Rect(self.x * CELL_SIZE[0], self.y * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0])
        if self.is_alive:
            if self.team == "good":
                color = BLUE
                appearance = pygame.image.load("../Textures/Lindwurm_Sketch.png").convert_alpha()
            elif self.team == "evil":
                color = RED
                appearance = pygame.image.load("../Textures/Larva_Sketch.png").convert_alpha()
            else:
                raise ValueError("No other alignment yet!")
            appearance = pygame.transform.scale(appearance, (CELL_SIZE[0], CELL_SIZE[0]))
            WINDOW.blit(appearance, (self.x * CELL_SIZE[0], self.y * CELL_SIZE[0]))

            # Affiche self.health à l'écran.
            pygame.draw.rect(WINDOW, RED, (int(CELL_SIZE[0] * (self.x + 11/12)), int(self.y * CELL_SIZE[0]), int(CELL_SIZE[0] * 1/12), int(CELL_SIZE[0])))
            pygame.draw.rect(WINDOW, GREEN, (int(CELL_SIZE[0] * (self.x + 11/12)), int(CELL_SIZE[0] * (self.y + 1 - self.health / 60)), int(CELL_SIZE[0] * 1/12), int(CELL_SIZE[0] * self.health / 60)))

            if self.is_selected:
                pygame.draw.rect(WINDOW, BLUE, (self.x * CELL_SIZE[0], self.y * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)
