import pygame
from abc import ABC, abstractmethod
import random
import os
import sys
import numpy as np

from var import *
from unit import *
from menu import *
from VictoryDisplay import *
from mana import *


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
        Construit le jeu avec la surface de la fenêtre et initialise la musique.

        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        """
        self.screen = screen
        self.good_units = [Royal(6, 3, "good"),  #liste et emplacements des joueurs gentils
                             Soldier(6, 2, "good"),
                             Soldier(6, 4, "good"),
                             Pauper(5, 2, "good"),
                             Pauper(5, 3, "good"),
                             Pauper(5, 4, "good")]

        self.evil_units = [Royal(0, 3, "evil"),  #liste et emplacement des joueurs méchants
                             Soldier(0, 2, "evil"),
                             Soldier(0, 4, "evil"),
                             Pauper(1, 2, "evil"),
                             Pauper(1, 3, "evil"),
                             Pauper(1, 4, "evil")]

        # On compte le nombre total de Pauper (utile pour le déclenchement de l'Easter Egg).
        self.PauperNumTot = 0
        for unit in self.evil_units + self.good_units:
            if isinstance(unit, Pauper):
                self.PauperNumTot = 6

        self.mana_src = [Mana(0, 0), Mana(6, 0), Mana(0, 6), Mana(6, 6), Mana(3, 0), Mana(3, 6)]  #liste constituée d'objet source mana placés à des positions fixe sur la grille

        self.no_death = 0 # Compteur de morts.
        
        # Initialisation de la musique
        pygame.mixer.init()
        self.music_file = "../Assets/game_music.mp3"  # Assurez-vous que ce fichier existe
        self.play_music(self.music_file)

    def play_music(self, music_file):
        """
        Joue une musique de fond en boucle.
        """
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.play(-1)  # -1 pour la lecture en boucle
            pygame.mixer.music.set_volume(VOLUME)  # Ajuste le volume
        except FileNotFoundError:
            print(f"Fichier audio introuvable : {music_file}")

    def team(self, unit):
        """
        Retourne -1 si unit est evil, +1 si unit est good.
        """
        if unit.team == "good":
            return 1
        if unit.team == "evil":
            return -1

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
        Heal = False # L'unité s'est-elle régénérée?
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
                    if not isinstance(selected_unit, Pauper):
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
                    # Si Pauper, l'unité peut attaquer puis se déplacer.
                    if isinstance(selected_unit, Pauper):
                        if event.key == pygame.K_LEFT and selected_unit.move_count < selected_unit.speed: # Si on veut se déplacer à gauche, qu'on a pas encore usé toute notre capacité de déplacement et qu'on n'a pas encore attaqué.
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
                        elif event.key == pygame.K_RIGHT and selected_unit.move_count < selected_unit.speed:
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
                        elif event.key == pygame.K_UP and selected_unit.move_count < selected_unit.speed:
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
                        elif event.key == pygame.K_DOWN and selected_unit.move_count < selected_unit.speed:
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

                    # On vérifie la condition de protection des attaques à distance.
                    for unit in self.evil_units + self.good_units:
                        if BOARD[unit.y][unit.x] == self.team(unit):
                            unit.protected = True
                        else:
                            unit.protected = False

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
                        Heal = selected_unit.heal(Heal, event, self)

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

                    pygame.time.Clock().tick(FPS)

    def rmv_dead(self, unit_set):
        """Renvoie la liste unit_set, mais sans les unités mortes."""
        no_dead = [unit for unit in unit_set if unit.is_alive]
        if no_dead == unit_set:  #commpare la liste des unités non mortes avec la liste d'origine
            self.no_death += 1  #si aucune unité n'est morte alors la varibale interne est incrémentée de 1
        else:
            self.no_death = 0  # si il y a des unités mortes, la variable interne est réinitialiser à 0
        return no_dead 

    def flip_display(self):
        """Affiche le jeu."""
        # Affiche la grille et met à jour les dimensions de la fenêtre. (cellules restent carrées même si l'écran est rectangulaire).
        self.screen.fill(BLACK)
        CELL_SIZE[0] = min(self.screen.get_width() // GRID_SIZE, self.screen.get_height() // GRID_SIZE)   # self.screen.get_width() // GRID_SIZE signifie la largeur de l'écran diviser par le nb cellules --> afin de déterminer la taille de la cellule
        WIDTH[0] = GRID_SIZE * CELL_SIZE[0]
        HEIGHT[0] = WIDTH[0]
        for x in range(0, GRID_SIZE):   #on dessine la grille
            for y in range(0, GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE[0], y * CELL_SIZE[0], CELL_SIZE[0], CELL_SIZE[0])
                col = [DARK_RED if BOARD[y][x] == -1 else DARK_GREEN if BOARD[y][x] == 1 else BLACK]
                pygame.draw.rect(self.screen, col[0], rect)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Affiche les unités
        for unit in self.good_units + self.evil_units:
            unit.draw(self.screen)   #chaque unité dessine sa propre représentation

        for mana_src in self.mana_src:
            mana_src.draw(self.screen)

        # Rafraîchit l'écran
        pygame.display.flip()

    def GameOver(self):
        # Renvoie True si un des camps est éliminé, et un str indiquant quel joueur a gagné.
        Good_alive = False # Les gentils sont-ils en vie?
        Evil_alive = False # Les méchants sont-ils en vie?
        NoSoldier = True # On vérifie que tous les Soldier sont morts (pour l'Eatser Egg).
        PauperNum = 0 # On vérifie que tous les Paupers sont encore en vie.
        if self.no_death >= NB_TURN_TIE * 4:
            NoWar = VictoryDisplay(self.screen) # Partie nulle si aucun mort pendant NB_TOUR_TIE tours!
            NoWar.show_no_war()
            return True
        for unit in self.evil_units + self.good_units:
            if unit.team == "evil":
                Evil_alive = True
            if unit.team == "good":
                Good_alive = True
            if isinstance(unit, Soldier): #signifie que si unité est de type solider
                NoSoldier = False # Il y a bien encore au moins un soldat.
            if isinstance(unit, Pauper):  #signifie que si unité est de type pauper
                PauperNum += 1  #paupernum est incrémenté de 1
        if not(Good_alive) and not(Evil_alive):  #si aucune des équipes est en vie, la partie est déclarée nulle
            Tie = VictoryDisplay(self.screen)
            Tie.show_tie()
            return True
        elif not Evil_alive:  #si les gentils ont gagnés
            GoodWon = VictoryDisplay(self.screen)
            GoodWon.show_good_won()
            return True
        elif not Good_alive:  #si les méchants ont gagnés
            EvilWon = VictoryDisplay(self.screen)
            EvilWon.show_evil_won()
            return True
        elif NoSoldier and PauperNum == self.PauperNumTot: # Condition du déclenchement de l'Easter Egg.
        #les soldats sont tous morts et les paupers sont vivant 
            # On vérifie maintenant que les Royal sont côte à côte grâce à la condition sur les positions.
            if ((self.evil_units[0].x == self.good_units[0].x + 1 or self.evil_units[0].x == self.good_units[0].x - 1) and self.evil_units[0].y == self.good_units[0].y) or (self.evil_units[0].x == self.good_units[0].x and (self.evil_units[0].y == self.good_units[0].y + 1 or self.evil_units[0].y == self.good_units[0].y - 1)):
                Easter = VictoryDisplay(self.screen)
                Easter.show_easter()
                return True
