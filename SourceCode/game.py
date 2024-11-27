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
        """Tour du joueur ayant les 'unit_set'."""
        # Sélection de l'unité à jouer.
        self.flip_display()
        selectionMade = False # Le joueur a-t-il sélectionné son unité?
        while not selectionMade:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = pygame.mouse.get_pos()
                    for unit in unit_set:
                        if unit.rect.collidepoint(click_pos): # Le joueur a sélectionné son unité.
                            selected_unit = unit
                            selectionMade = True
                            selected_unit.is_selected = True
                            self.flip_display()
                            break

        # Tant que l'unité n'a pas terminé son tour
        has_acted = False
        Deplacer = False # L'unité a-t-elle bougée?
        while not has_acted:
            # Important: cette boucle permet de gérer les événements Pygame
            for event in pygame.event.get():

                # Gestion de la fermeture de la fenêtre
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Gestion des touches du clavier
                if event.type == pygame.KEYDOWN:

                    # Déplacement (touches fléchées)
                    dx, dy = 0, 0
                    collide = False # L'unité va-t-elle percuter une autre unité?
                    if event.key == pygame.K_LEFT and selected_unit.move_count < selected_unit.speed:
                        dx = -1
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
                    elif event.key == pygame.K_RIGHT and selected_unit.move_count < selected_unit.speed:
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
                    elif event.key == pygame.K_UP and selected_unit.move_count < selected_unit.speed:
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
                    elif event.key == pygame.K_DOWN and selected_unit.move_count < selected_unit.speed:
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

                    selected_unit.move(dx, dy)
                    self.flip_display()

                    # Attaque (simple ou berserk, d'une case)

                    if not(Deplacer) and event.key == pygame.K_z:
                        target = [selected_unit.x, selected_unit.y - 1]
                        pygame.draw.rect(WINDOW, GREEN, (target[0] * CELL_SIZE, target[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    elif not(Deplacer) and event.key == pygame.K_q:
                        target = [selected_unit.x - 1, selected_unit.y]
                        pygame.draw.rect(WINDOW, GREEN, (target[0] * CELL_SIZE, target[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    elif not(Deplacer) and event.key == pygame.K_s:
                        target = [selected_unit.x, selected_unit.y + 1]
                        pygame.draw.rect(WINDOW, GREEN, (target[0] * CELL_SIZE, target[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                    elif not(Deplacer) and event.key == pygame.K_d:
                        target = [selected_unit.x + 1, selected_unit.y]
                        pygame.draw.rect(WINDOW, GREEN, (target[0] * CELL_SIZE, target[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                    pygame.display.update()

                    # Fin de tour
                    if event.key == pygame.K_RETURN:
                        has_acted = True
                        selected_unit.is_selected = False
                        selected_unit.move_count = 0
                        break

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
        game.handle_turn(game.good_units) # Tour des gentils.


if __name__ == "__main__":
    main()
