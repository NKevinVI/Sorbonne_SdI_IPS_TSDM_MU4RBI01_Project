import pygame
from abc import ABC, abstractmethod
import random
import os
import sys
import numpy as np

from var import *
from game import *
from unit import *
from menu import *
from VictoryDisplay import *
from mana import *


class Main:
    def __init__(self):
        self.reset = False # Should we reset the game?

        # Initialisation de Pygame
        pygame.init()

        # Instanciation de la fenêtre
        screen = pygame.display.set_mode((WIDTH[0], HEIGHT[0]), pygame.RESIZABLE)
        pygame.display.set_caption("Draconic Generations") # Titre de la fenêtre.

        # Gestion du menu de départ.
        menu = Menu(screen)
        menu.display()

        # Instanciation du jeu
        game = Game(screen)

        # Boucle principale du jeu
        while True:
            game.handle_turn(game.evil_units) # Tour des méchants pas beaux!

            game.evil_units = game.rmv_dead(game.evil_units) # Supprimer les macchabées!
            game.good_units = game.rmv_dead(game.good_units) # Supprimer les macchabées!

            self.reset = game.GameOver()
            if self.reset:
                self.restart()


            game.handle_turn(game.good_units) # Tour des gentils.

            game.evil_units = game.rmv_dead(game.evil_units) # Supprimer les macchabées!
            game.good_units = game.rmv_dead(game.good_units) # Supprimer les macchabées!

            self.reset = game.GameOver()
            if self.reset:
                self.restart()

    def restart(self):
        """
        Restart the entire game.
        """
        self.__init__()


if __name__ == "__main__":
    main = Main()
