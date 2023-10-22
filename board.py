from tkinter import *
from dice import *
from ex12_utils import *


class Board:
    """
    The board of the game. The board appears in a designated frame on the
    window and is constructed from 4x4 buttons (Dice objects) according to
    the str_board parameter that it receives when created (a 2d array with
    strings as it's elements, representing the letters on each button).
    """
    def __init__(self, window, str_board, word_var=None):
        self.__window = window
        self.__board_frame = Frame(window, height=500, width=500,
                                   highlightbackground="light blue",
                                   highlightthickness=2)
        self.__word_var = word_var
        self.__last_pressed = tuple()  # coordinates of last pressed dice
        self.__dice_board = self.initiate_dice(str_board)
        self.__path = list()  # will contain all pressed dice objects

    def initiate_dice(self, str_board):
        board = list()  # matrix - will contain the dice created
        row = list()  # a row in the matrix
        for row_ind in range(len(str_board)):
            for col_ind in range(len(str_board)):
                # get the string in current index:
                letter = str_board[row_ind][col_ind]
                # create Dice object with the string as it's label:
                cur_dice = Dice(self.__board_frame, letter, (row_ind, col_ind))
                # get button field of Dice object:
                cur_button = cur_dice.get_dice_button()
                cur_button.bind("<Button-1>", lambda event, a=cur_dice,
                                       b=cur_dice.get_coordinates():
                                       self.update_click(a, b))
                cur_button.grid(row=row_ind, column=col_ind)
                row.append(cur_dice)
            board.append(row)
        return board

    def reset_board(self, str_board):
        self.__dice_board = self.initiate_dice(str_board)

    def update_click(self, dice, coordinates):
        # check if dice clicked is not an invalid click:
        # 1. check that last_pressed is not None (if it is, everything's valid)
        # 2. check if the move skips over dice
        # 3. check if the dice has been clicked before
        if self.__last_pressed and \
                (coordinates not in get_possible_moves(
                    self.__last_pressed).values()
                 or dice.get_state()):
            dice.turn_red()
            self.__window.after(1, dice.turn_red)
            self.__window.after(200, dice.turn_back)
            return
        self.__last_pressed = coordinates
        self.__path.append(dice)
        self.__word_var.set(self.__word_var.get() + dice.get_letter())
        dice.set_state(True)

    def get_board_frame(self):
        return self.__board_frame

    def get_path(self):
        return self.__path

    def get_word_var(self):
        return self.__word_var

    def set_path(self, val):
        self.__path = val

    def set_last_pressed(self, val):
        self.__last_pressed = val

    def set_word_var(self, val):
        self.__word_var = val
