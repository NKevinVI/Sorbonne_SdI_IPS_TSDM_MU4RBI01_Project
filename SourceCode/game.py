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
        
        # Grille de jeu
        self.grid_size = WIDTH // CELL_SIZE
        self.grid = [[None for _ in range(self.grid_size)] for _ in range(self.grid_size)]


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
        
        # Positionner les unités dans la grille
        for unit in self.good_units + self.evil_units:
            self.grid[unit.y][unit.x] = unit


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
    
    def is_cell_free(self, x, y):
        """Vérifie si une case est libre."""
        if not (0 <= x < WIDTH // CELL_SIZE and 0 <= y < HEIGHT // CELL_SIZE):
            return False  # En dehors des limites
        for unit in self.good_units + self.evil_units:
            if unit.x == x and unit.y == y:
                return False  # Une unité occupe déjà cette case
        return True

    def move_unit(self, unit, dx, dy):
        """Déplace une unité si la case cible est libre."""
        new_x = unit.x + dx
        new_y = unit.y + dy

        if self.is_cell_free(new_x, new_y):
            # Libérer la case actuelle
            self.grid[unit.y][unit.x] = None

            # Déplacer l'unité
            unit.x = new_x
            unit.y = new_y

            # Occuper la nouvelle case
            self.grid[new_y][new_x] = unit
            return True
        return False

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
        
        
    def check_victory(game):
        """
        Vérifie les conditions de victoire.
        Retourne le gagnant : 'good', 'evil', ou None si la partie continue.
        """
        if not game.evil_units:  # Tous les ennemis sont éliminés
            return "good"
        if not game.good_units:  # Tous les alliés sont éliminés
            return "evil"
        return None


def show_victory_screen(screen, winner):
        """
        Affiche l'écran de victoire.
        
        Paramètres
        ----------
        screen : pygame.Surface
            La surface de la fenêtre du jeu.
        winner : str
            Le gagnant ('good' ou 'evil').
        """
        # Couleur de fond
        screen.fill(BLACK)
    
        # Message de victoire
        font = pygame.font.Font(None, 74)
        message = f"Victoire des {'bons' if winner == 'good' else 'mauvais'}!"
        text = font.render(message, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
        screen.blit(text, text_rect)
    
        # Instructions
        small_font = pygame.font.Font(None, 36)
        instructions = small_font.render("Appuyez sur R pour rejouer ou Q pour quitter", True, WHITE)
        instructions_rect = instructions.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(instructions, instructions_rect)
    
        # Met à jour l'affichage
        pygame.display.flip()
    
        # Attendre l'entrée de l'utilisateur
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Rejouer
                        return "restart"
                    if event.key == pygame.K_q:  # Quitter
                        pygame.quit()
                        exit()



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
        
        # Vérifier la victoire
        winner = check_victory(game)
        if winner:
            action = show_victory_screen(screen, winner)
            if action == "restart":
                break  # Redémarre la partie


if __name__ == "__main__":
    main()
