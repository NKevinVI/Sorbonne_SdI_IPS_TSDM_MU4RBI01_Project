import pygame
import random
import os
import sys

from unit import *
from mana import *
from menu import *
from VictoryDisplay import *


class Game:
    """
    Classe pour représenter le jeu.

    ...
    Attributs
    ---------
    screen: pygame.Surface
        La surface de la fenêtre du jeu.
    good_units : list[Unit]
        La liste des unités du second joueur.
    evil_units : list[Unit]
        La liste des unités de premier joueur.
    """

    def __init__(self, screen):
        """
        Construit le jeu avec la surface de la fenêtre.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.good_units = [Royal(6, 3, "good"),
                             Soldier(6, 2, "good"),
                             Soldier(6, 4, "good"),
                             Pauper(5, 2, "good"),
                             Pauper(5, 3, "good"),
                             Pauper(5, 4, "good")]

        self.evil_units = [Royal(0, 3, "evil"),
                             Soldier(0, 2, "evil"),
                             Soldier(0, 4, "evil"),
                             Pauper(1, 2, "evil"),
                             Pauper(1, 3, "evil"),
                             Pauper(1, 4, "evil")]

        self.mana_src = [Mana(0, 0), Mana(6, 0), Mana(0, 6), Mana(6, 6), Mana(3, 0), Mana(3, 6)]

    def handle_turn(self, unit_set):
        """Tour du joueur ayant les 'unit_set' comme unités."""
        # Sélection de l'unité à jouer.
        self.flip_display() # On met à jour l'écran.
        selectionMade = False # Le joueur a-t-il sélectionné son unité?
        while not selectionMade:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: # Gestion de la fermeture de la fenêtre.
                    pygame.quit()
                    exit()
                if event.type == pygame.VIDEORESIZE:
                    self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.flip_display()
                if event.type == pygame.KEYDOWN:
                    self.flip_display() # Met à jour l'écran.
                if event.type == pygame.MOUSEBUTTONDOWN: # Le joueur a-t-il cliqué avec la souris?
                    click_pos = pygame.mouse.get_pos() # On récupère la position du curseur de la souris.
                    for unit in unit_set:
                        if unit.rect.collidepoint(click_pos): # Le joueur a cliqué sur l'unité, donc l'a sélectionnée.
                            selected_unit = unit
                            selectionMade = True
                            selected_unit.is_selected = True
                            self.flip_display()
                            break

        # Tant que l'unité n'a pas terminé son tour
        has_acted = False # L'unité a-t-elle joué?
        Deplacer = False # L'unité a-t-elle bougée?
        Attaque = False # L'unité a-t-elle attaquée?
        target = [selected_unit.x, selected_unit.y] # Cible par défaut: soi-même.
        mouse_pos = [None, None] # Position du curseur.
        while not has_acted:
            # Important: cette boucle permet de gérer les événements Pygame
            for event in pygame.event.get():

                # Gestion de la fermeture de la fenêtre
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == pygame.VIDEORESIZE:
                    # self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                    self.flip_display()

                # Gestion des touches du clavier
                if event.type == pygame.KEYDOWN:
                    dx, dy = 0, 0 # Les potentiels de déplacement. À chaque déplacement de la part du joueur, l'unité se déplace de dx et dy sur la grille.

                    collide = False # L'unité va-t-elle percuter une autre unité?

                    # Gestion des déplacements.
                    if event.key == pygame.K_LEFT and selected_unit.move_count < selected_unit.speed and not(Attaque): # Si on veut se déplacer à gauche, qu'on a pas encore usé toute notre capacité de déplacement et qu'on n'a pas encore attaqué.
                        dx = -1 # Potentiel déplacement de 1 case vers la gauche.
                        if selected_unit.x + dx < 0: # Sommes-nous en situation de collision avec un mur?
                            collide = True
                        else:
                            for unit in self.good_units + self.evil_units:
                                if unit.x == selected_unit.x + dx and unit.y == selected_unit.y + dy: # Sommes-nous en situation de collision avec une autre unité?
                                    collide = True
                        if not collide: # Si pas de collision.
                            selected_unit.move_count += 1 # La créature est considérée comme s'étant déplacée de 1.
                            Deplacer = True # Elle s'est déplacée.
                        else: # Sinon, on annule le déplacement.
                            dx = 0
                            dy = 0
                    elif event.key == pygame.K_RIGHT and selected_unit.move_count < selected_unit.speed and not(Attaque):
                        dx = 1
                        if selected_unit.x + dx > GRID_SIZE - 1:
                            collide = True
                        else:
                            for unit in self.good_units + self.evil_units:
                                if unit.x == selected_unit.x + dx and unit.y == selected_unit.y + dy:
                                    collide = True
                        if not collide:
                            selected_unit.move_count += 1
                            Deplacer = True
                        else:
                            dx = 0
                            dy = 0
                    elif event.key == pygame.K_UP and selected_unit.move_count < selected_unit.speed and not(Attaque):
                        dy = -1
                        if selected_unit.y + dy < 0:
                            collide = True
                        else:
                            for unit in self.good_units + self.evil_units:
                                if unit.x == selected_unit.x + dx and unit.y == selected_unit.y + dy:
                                    collide = True
                        if not collide:
                            selected_unit.move_count += 1
                            Deplacer = True
                        else:
                            dx = 0
                            dy = 0
                    elif event.key == pygame.K_DOWN and selected_unit.move_count < selected_unit.speed and not(Attaque):
                        dy = 1
                        if selected_unit.y + dy > GRID_SIZE - 1:
                            collide = True
                        else:
                            for unit in self.good_units + self.evil_units:
                                if unit.x == selected_unit.x + dx and unit.y == selected_unit.y + dy:
                                    collide = True
                        if not collide:
                            selected_unit.move_count += 1
                            Deplacer = True
                        else:
                            dx = 0
                            dy = 0

                    # On effectue les déplacements visuellement.
                    selected_unit.move(dx, dy, self)

                    # Le mana!
                    if dx != 0 or dy != 0:
                        for mana in self.mana_src:
                            if selected_unit.x == mana.x and selected_unit.y == mana.y:
                                mana.absorbed(selected_unit)
                                self.flip_display()

                    # Attaque (simple): visée.
                    target = selected_unit.attack_show(target, Attaque, Deplacer, event)

                    # Attaque (simple): échange de dégâts.
                    Attaque = selected_unit.attack_simple(self.evil_units, self.good_units, Attaque, Deplacer, event, target, self)

                    # Régénération, si Pauper.
                    if isinstance(selected_unit, Pauper):
                        Attaque = selected_unit.heal(Attaque, Deplacer, event, self) # La régénération est traitée comme une attaque. Ne jugez pas, SVP.

                    # Attaque de zone, si Soldier. Gérée principalement par Game.
                    if isinstance(selected_unit, Soldier):
                        if event.key == pygame.K_x and not(Deplacer) and not(Attaque):
                            target = [selected_unit.x, selected_unit.y]
                            atta = True # Being attacking.
                            pygame.draw.rect(WINDOW, RED, (target[0] * CELL_SIZE[0], target[1] * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)
                            if (target[0] + 1) * CELL_SIZE[0] < WIDTH[0]:
                                pygame.draw.rect(WINDOW, RED, ((target[0] + 1) * CELL_SIZE[0], target[1] * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)
                            if (target[0] - 1) * CELL_SIZE[0] >= 0:
                                pygame.draw.rect(WINDOW, RED, ((target[0] - 1) * CELL_SIZE[0], target[1] * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)
                            if (target[1] + 1) * CELL_SIZE[0] < HEIGHT[0]:
                                pygame.draw.rect(WINDOW, RED, (target[0] * CELL_SIZE[0], (target[1] + 1) * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)
                            if (target[1] - 1) * CELL_SIZE[0] >= 0:
                                pygame.draw.rect(WINDOW, RED, (target[0] * CELL_SIZE[0], (target[1] - 1) * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)
                            pygame.display.update()
                            while atta:
                                for event_ in pygame.event.get():
                                    if event_.type == pygame.QUIT:
                                        pygame.quit()
                                        exit()
                                    if event_.type == pygame.KEYDOWN:
                                        self.flip_display()
                                        if event_.key == pygame.K_LEFT:
                                            target[0] -= 1
                                        if event_.key == pygame.K_RIGHT:
                                            target[0] += 1
                                        if event_.key == pygame.K_UP:
                                            target[1] -= 1
                                        if event_.key == pygame.K_DOWN:
                                            target[1] += 1

                                        # Vérification qu'on ne se barre pas trop loin.
                                        if target[0] < 0:
                                            target[0] = 0
                                        if target[0] >= GRID_SIZE:
                                            target[0] = GRID_SIZE - 1
                                        if target[1] < 0:
                                            target[1] = 0
                                        if target[1] >= GRID_SIZE:
                                            target[1] = GRID_SIZE - 1

                                        pygame.draw.rect(WINDOW, RED, (target[0] * CELL_SIZE[0], target[1] * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)
                                        if (target[0] + 1) * CELL_SIZE[0] < WIDTH[0]:
                                            pygame.draw.rect(WINDOW, RED, ((target[0] + 1) * CELL_SIZE[0], target[1] * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)
                                        if (target[0] - 1) * CELL_SIZE[0] >= 0:
                                            pygame.draw.rect(WINDOW, RED, ((target[0] - 1) * CELL_SIZE[0], target[1] * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)
                                        if (target[1] + 1) * CELL_SIZE[0] < HEIGHT[0]:
                                            pygame.draw.rect(WINDOW, RED, (target[0] * CELL_SIZE[0], (target[1] + 1) * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)
                                        if (target[1] - 1) * CELL_SIZE[0] >= 0:
                                            pygame.draw.rect(WINDOW, RED, (target[0] * CELL_SIZE[0], (target[1] - 1) * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0]), 2)
                                        pygame.display.update()
                                        if event_.key == pygame.K_ESCAPE:
                                            atta = False
                                        if event_.key == pygame.K_SPACE:
                                            for unit in self.good_units + self.evil_units:
                                                selected_unit.attack_special(target, unit)
                                            atta = False
                                            Attaque = True
                            self.flip_display()

                    # Attaque berserk, si Royal.
                    if isinstance(selected_unit, Royal):
                        Attaque = selected_unit.attack_berserk(self.evil_units, self.good_units, Attaque, Deplacer, event, target, self)

                    # Fin de tour
                    if event.key == pygame.K_RETURN:
                        has_acted = True
                        selected_unit.is_selected = False
                        Attaque = False
                        selected_unit.move_count = 0
                        mouse_pos = None
                        break

    def rmv_dead(self, unit_set):
        """Renvoie la liste unit_set, mais sans les unités mortes."""
        return [unit for unit in unit_set if unit.is_alive]

    def flip_display(self):
        """Affiche le jeu."""

        # Affiche la grille et met à jour les dimensions de la fenêtre.
        self.screen.fill(BLACK)
        CELL_SIZE[0] = min(self.screen.get_width() // GRID_SIZE, self.screen.get_height() // GRID_SIZE)
        WIDTH[0] = GRID_SIZE * CELL_SIZE[0]
        HEIGHT[0] = WIDTH[0]
        for x in range(0, GRID_SIZE):
            for y in range(0, GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE[0], y * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0])
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Affiche les unités
        for unit in self.good_units + self.evil_units:
            unit.draw(self.screen)

        for mana_src in self.mana_src:
            mana_src.draw(self.screen)

        # Rafraîchit l'écran
        pygame.display.flip()

    def GameOver(self, unit_set):
        # Renvoie True si un des camps est éliminé, et un str indiquant quel joueur a gagné.
        Good_alive = False # Les gentils sont-ils en vie?
        Evil_alive = False # Les méchants sont-ils en vie?
        for unit in unit_set:
            if unit.team == "evil":
                Evil_alive = True
            if unit.team == "good":
                Good_alive = True
        if not(Good_alive) and not(Evil_alive):
            Tie = VictoryDisplay(self.screen)
            Tie.show_tie()
        elif not Evil_alive:
            GoodWon = VictoryDisplay(self.screen)
            GoodWon.show_good_won()
        elif not Good_alive:
            EvilWon = VictoryDisplay(self.screen)
            EvilWon.show_evil_won()

def main():
    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH[0], HEIGHT[0]), pygame.RESIZABLE)
    pygame.display.set_caption("Draconic Generations") # Titre de la fenêtre.

    # Gestion du menu de départ.
    menu = Menu(screen)
    menu.display()
    # if not menu.show_menu():
    #     return

    # Instanciation du jeu
    game = Game(screen)

    # Boucle principale du jeu
    while True:
        game.GameOver(game.evil_units + game.good_units)
        game.handle_turn(game.evil_units) # Tour des méchants pas beaux!

        game.evil_units = game.rmv_dead(game.evil_units) # Supprimer les macchabées!
        game.good_units = game.rmv_dead(game.good_units) # Supprimer les macchabées!

        game.GameOver(game.evil_units + game.good_units)


        game.handle_turn(game.good_units) # Tour des gentils.

        game.evil_units = game.rmv_dead(game.evil_units) # Supprimer les macchabées!
        game.good_units = game.rmv_dead(game.good_units) # Supprimer les macchabées!

        game.GameOver(game.evil_units + game.good_units)


if __name__ == "__main__":
    main()
