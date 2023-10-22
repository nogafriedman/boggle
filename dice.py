from tkinter import *
import time

class Dice:
    """
    The board's buttons - Each dice has a string that appears on it in the
    game, and has three states:  white (unpressed), black (pressed) and red
    (invalid click - turns red for a few seconds and then goes back to black).
    """
    def __init__(self, root, letter, coordinates):
        self.__root = root
        self.__photo_unpressed = PhotoImage(file="Resources/Images/boggle_cube.png")
        self.__photo_pressed = PhotoImage(file="Resources/Images/cube_pressed.png")
        self.__photo_invalid = PhotoImage(file="Resources/Images/cube_invalid.png")
        self.__dice_button = Button(root, image=self.__photo_unpressed,
                                    height=100, width=100, text=letter,
                                    font=("Tahoma", 50),
                                    compound="center")
        self.__state = False  # True if dice is pressed, False if not
        self.__letter = letter
        self.__coordinates = coordinates

    def get_state(self):
        return self.__state

    def get_dice_button(self):
        return self.__dice_button

    def get_letter(self):
        return self.__letter

    def get_coordinates(self):
        return self.__coordinates

    def set_state(self, bool):
        # presses the dice if bool=True, unpresses the dice if bool=False
        if not bool:
            self.__dice_button.config(image=self.__photo_unpressed)
        if bool:
            self.__dice_button.config(image=self.__photo_pressed)
        self.__state = bool
        return self.__state

    def turn_red(self):
        # makes the dice red for a few seconds if the click was invalid
        self.__dice_button.config(image=self.__photo_invalid)
        return

    def turn_back(self):
        # if dice was clicked when already clicked before -
        # change to pressed color:
        if self.__state:
            self.__dice_button.config(image=self.__photo_pressed)
        # if dice was clicked but wasn't on the valid coordinates -
        # change to unpressed color:
        else:
            self.__dice_button.config(image=self.__photo_unpressed)
