from game_logic import *
from gui_manager import *


class Boggle:
    """
    The controller of the game. Creates a Game object (responsible for the
    Boggle game logic) and a GUIManager object (a tkinter root that creates a
    screen to run and visualize the game).
    """
    def __init__(self):
        # initialize game logic:
        self.__game_logic = Game()
        # initialize the game window where the game will be displayed:
        self.__gui = GUIManager(self.__game_logic)


if __name__ == '__main__':
    initiate_game = Boggle()
