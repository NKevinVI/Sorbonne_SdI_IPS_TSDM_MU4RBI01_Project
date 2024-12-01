import pygame
import random

from unit import *


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
        while not has_acted:
            # Important: cette boucle permet de gérer les événements Pygame
            for event in pygame.event.get():

                # Gestion de la fermeture de la fenêtre
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Gestion des touches du clavier
                if event.type == pygame.KEYDOWN:

                    dx, dy = 0, 0 # Les potentiels de déplacement. À chaque déplacement de la part du joueur, l'unité se déplace de dx et dy sur la grille.

                    collide = False # L'unité va-t-elle percuter une autre unité?

                    # Gestion des déplacements.
                    if event.key == pygame.K_LEFT and selected_unit.move_count < selected_unit.speed and not(Attaque): # Si on veut se déplacer à gauche, qu'on a pas encore usé toute notre capacité de déplacement et qu'on n'a pas encore attaqué.
                        dx = -1 # Potentiel déplacement de 1 case vers la gauche.
                        if selected_unit.x + dx > GRID_SIZE - 1 or selected_unit.x + dx < 0 or selected_unit.y + dy > GRID_SIZE - 1 or selected_unit.y + dy < 0: # Sommes-nous en situation de collision avec un mur?
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
                        if selected_unit.x + dx > GRID_SIZE - 1 or selected_unit.x + dx < 0 or selected_unit.y + dy > GRID_SIZE - 1 or selected_unit.y + dy < 0:
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
                        if selected_unit.x + dx > GRID_SIZE - 1 or selected_unit.x + dx < 0 or selected_unit.y + dy > GRID_SIZE - 1 or selected_unit.y + dy < 0:
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
                        if selected_unit.x + dx > GRID_SIZE - 1 or selected_unit.x + dx < 0 or selected_unit.y + dy > GRID_SIZE - 1 or selected_unit.y + dy < 0:
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

                    # Attaque (simple): visée.
                    target = selected_unit.attack_show(target, Attaque, Deplacer, event)

                    # Attaque (simple): échange de dégâts.
                    Attaque = selected_unit.attack_simple(self.evil_units, self.good_units, Attaque, Deplacer, event, target, self)

                    if isinstance(selected_unit, Pauper):
                        Attaque = selected_unit.heal(Attaque, Deplacer, event, self) # La régénération est traitée comme une attaque. Ne jugez pas, SVP.

                    # # Attaque spéciale (soldier) (maintenir X).
                    # pressed_keys = pygame.key.get_pressed()
                    # if pressed_keys[pygame.K_x] and isinstance(selected_unit, Soldier):
                    #     mouse_pos = pygame.mouse.get_pos()
                    #     if

                    # On met à jour l'impression écran.

                    # Fin de tour
                    if event.key == pygame.K_RETURN:
                        has_acted = True
                        selected_unit.is_selected = False
                        Attaque = False
                        selected_unit.move_count = 0
                        break

    def rmv_dead(self, unit_set):
        """Renvoie la liste unit_set, mais sans les unités mortes."""
        return [unit for unit in unit_set if unit.health > 0]

    def flip_display(self):
        """Affiche le jeu."""

        # Affiche la grille
        self.screen.fill(BLACK)
        for x in range(0, WIDTH, CELL_SIZE):
            for y in range(0, HEIGHT, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Affiche les unités
        for unit in self.good_units + self.evil_units:
            unit.draw(self.screen)

        # Rafraîchit l'écran
        pygame.display.flip()


def main():
    # Initialisation de Pygame
    pygame.init()

    # Instanciation de la fenêtre
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Draconic Generations")

    # Instanciation du jeu
    game = Game(screen)

    # Boucle principale du jeu
    while True:
        game.handle_turn(game.evil_units) # Tour des méchants pas beaux!
        game.evil_units = game.rmv_dead(game.evil_units) # Supprimer les macchabées!
        game.good_units = game.rmv_dead(game.good_units) # Supprimer les macchabées!
        game.handle_turn(game.good_units) # Tour des gentils.
        game.evil_units = game.rmv_dead(game.evil_units) # Supprimer les macchabées!
        game.good_units = game.rmv_dead(game.good_units) # Supprimer les macchabées!


if __name__ == "__main__":
    main()
