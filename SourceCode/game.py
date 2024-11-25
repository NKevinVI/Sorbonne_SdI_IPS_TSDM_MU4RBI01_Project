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
        self.good_units = [Unit(6, 3, "good", "royal"),
                             Unit(6, 2, "good", "soldier"),
                             Unit(6, 4, "good", "soldier"),
                             Unit(5, 2, "good", "pauper"),
                             Unit(5, 3, "good", "pauper"),
                             Unit(5, 4, "good", "pauper")]

        self.evil_units = [Unit(0, 3, "evil", "royal"),
                             Unit(0, 2, "evil", "soldier"),
                             Unit(0, 4, "evil", "soldier"),
                             Unit(1, 2, "evil", "pauper"),
                             Unit(1, 3, "evil", "pauper"),
                             Unit(1, 4, "evil", "pauper")]

    def handle_good_turn(self):
        """Tour du joueur 'good'"""
        for selected_unit in self.good_units:

            # Tant que l'unité n'a pas terminé son tour
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
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
                        if event.key == pygame.K_LEFT and selected_unit.move_count < selected_unit.speed:
                            dx = -1
                            selected_unit.move_count += 1
                        elif event.key == pygame.K_RIGHT and selected_unit.move_count < selected_unit.speed:
                            dx = 1
                            selected_unit.move_count += 1
                        elif event.key == pygame.K_UP and selected_unit.move_count < selected_unit.speed:
                            dy = -1
                            selected_unit.move_count += 1
                        elif event.key == pygame.K_DOWN and selected_unit.move_count < selected_unit.speed:
                            dy = 1
                            selected_unit.move_count += 1

                        selected_unit.move(dx, dy)
                        self.flip_display()

                        # Attaque (touche espace) met fin au tour
                        # if event.key == pygame.K_SPACE:
                        #     for good in self.good_units:
                        #         if abs(selected_unit.x - good.x) <= 1 and abs(selected_unit.y - good.y) <= 1:
                        #             selected_unit.attack(good)
                        #             if good.health <= 0:
                        #                 self.good_units.remove(good)

                        # End of turn
                        if event.key == pygame.K_RETURN:
                            has_acted = True
                            selected_unit.is_selected = False
                            selected_unit.move_count = 0
                            break

    def handle_evil_turn(self):
        """Tour du joueur 'evil'"""
        for selected_unit in self.evil_units:

            # Tant que l'unité n'a pas terminé son tour
            has_acted = False
            selected_unit.is_selected = True
            self.flip_display()
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
                        if event.key == pygame.K_LEFT and selected_unit.move_count < selected_unit.speed:
                            dx = -1
                            selected_unit.move_count += 1
                        elif event.key == pygame.K_RIGHT and selected_unit.move_count < selected_unit.speed:
                            dx = 1
                            selected_unit.move_count += 1
                        elif event.key == pygame.K_UP and selected_unit.move_count < selected_unit.speed:
                            dy = -1
                            selected_unit.move_count += 1
                        elif event.key == pygame.K_DOWN and selected_unit.move_count < selected_unit.speed:
                            dy = 1
                            selected_unit.move_count += 1

                        selected_unit.move(dx, dy)
                        self.flip_display()

                        # Attaque (touche espace) met fin au tour
                        # if event.key == pygame.K_SPACE:
                        #     for good in self.good_units:
                        #         if abs(selected_unit.x - good.x) <= 1 and abs(selected_unit.y - good.y) <= 1:
                        #             selected_unit.attack(good)
                        #             if good.health <= 0:
                        #                 self.good_units.remove(good)

                        # End of turn
                        if event.key == pygame.K_RETURN:
                            has_acted = True
                            selected_unit.is_selected = False
                            selected_unit.move_count = 0
                            break

    # def handle_enemy_turn(self):
    #     """IA très simple pour les ennemis."""
    #     for enemy in self.enemy_units:
    #
    #         # Déplacement aléatoire
    #         target = random.choice(self.player_units)
    #         dx = 1 if enemy.x < target.x else -1 if enemy.x > target.x else 0
    #         dy = 1 if enemy.y < target.y else -1 if enemy.y > target.y else 0
    #         enemy.move(dx, dy)
    #
    #         # Attaque si possible
    #         if abs(enemy.x - target.x) <= 1 and abs(enemy.y - target.y) <= 1:
    #             enemy.attack(target)
    #             if target.health <= 0:
    #                 self.player_units.remove(target)

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
        game.handle_evil_turn()
        game.handle_good_turn()


if __name__ == "__main__":
    main()
