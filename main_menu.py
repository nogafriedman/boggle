from tkinter import *
from dice import *
from ex12_utils import *
from game_logic import *

MAIN_TITLE = "Welcome To Boggle!"


class MainMenu:
    """
    This class is responsible for holding the tkinter objects related to
    the main menu, and is created by the GUIManager at the start of the game.
    It's separated from the GUIManager class for easier control of the two,
    since they both represent different "displays" of the game.
    """
    def __init__(self, root, window, game_obj):
        self.__root = root
        self.__current_window = window
        self.__game = game_obj
        # images:
        self.exit_image = PhotoImage(file="Resources/Images/exit.png")
        self.trophy_image = PhotoImage(file="Resources/Images/trophy.png")
        self.first_image = PhotoImage(file="Resources/Images/first.png")
        self.second_image = PhotoImage(file="Resources/Images/second.png")
        self.third_image = PhotoImage(file="Resources/Images/third.png")
        # graphics:
        self.frame = Frame(root, height=600, width=500, bg="white")
        self.header = Label(self.frame, height=1, width=30, text=MAIN_TITLE,
                            bg="white", font=("Tahoma", 30))
        self.exit_button = Button(self.frame, height=50, width=50,
                                  image=self.exit_image, bg="white",
                                  command=self.__root.destroy)
        # initialize score board:
        self.__high_scores = self.load_score_board()
        self.__score_board = Frame(self.frame, height = 100, width = 100)
        self.__hof_header = Label(self.__score_board, image=self.trophy_image,
                                  compound="left", bg="white", height=40, width=600,
                                  text="Score Board", font=("Tahoma", 20))
        self.__hof_first = Label(self.__score_board, image=self.first_image,
                                 compound="left", bg="white", height=60, width=600,
                                 text=str(self.__high_scores[0][0] + "   Score: "
                                          + str(self.__high_scores[0][1])),
                                 font=("Tahoma", 20))
        self.__hof_second = Label(self.__score_board, image=self.second_image,
                                  compound="left", bg="white", height=60, width=600,
                                  text=str(self.__high_scores[1][0] + "   Score: " +
                                           str(self.__high_scores[1][1])),
                                  font=("Tahoma", 20))
        self.__hof_third = Label(self.__score_board, image=self.third_image,
                                 compound="left", bg="white", height=60, width=600,
                                 text=str(self.__high_scores[2][0] + "   Score: "
                                          + str(self.__high_scores[2][1])),
                                 font=("Tahoma", 20))
        self.init_score_board()
        self.update_score_board()
        # initialize enter name frame
        self.__enter_name_frame = Frame(self.frame, height = 30, width = 50, bg="white")
        self.__ask_name = Label(self.__enter_name_frame, height=1, width=25,
                            text="Please Insert Name", bg="white", font=("Tahoma", 20))
        self.__enter_name = Text(self.__enter_name_frame, height = 2, width = 25,
                                 bg = "light blue")
        self.__play_button = Button(self.__enter_name_frame, text="Start Game",
                                height=1, width=10, font=("Tahoma", 30),
                                    bg="light green", command=self.start_game)
        self.init_name_frame()
        self.init_main_menu()

    def init_score_board(self):
        self.__hof_header.grid()
        self.__hof_first.grid()
        self.__hof_second.grid()
        self.__hof_third.grid()

    def init_main_menu(self):
        self.header.grid(sticky=N)
        self.exit_button.grid(sticky=NE)
        self.__score_board.grid(sticky=NW)
        self.__enter_name_frame.grid(padx=1, pady=4)

    def init_name_frame(self):
        self.__ask_name.pack()
        self.__enter_name.pack()
        self.__play_button.pack()

    def start_game(self):
        name = self.__enter_name.get("1.0", END)
        # deal with empty strings that could cause trouble with file load:
        invalid_names = ["", "\n", "\n\n"]
        if name in invalid_names or "\n" in name[:-2]:
            name = "No_Name "
        # deal with names entered with spaces:
        name = name.replace(' ', '_')
        self.__game.set_player_name(name[:-1])
        self.__current_window.start_game()

    def sort_by_second(self, tup1, tup2):
        # helper function for update_score
        return int(tup1[1]) < int(tup2[1])

    def update_score(self, name, score):
        # append new score to list:
        self.__high_scores.append((name, score))
        new_scores = list()
        # convert all str scores to int in order to sort them:
        for ind in range(len(self.__high_scores)):
            new_scores.append((self.__high_scores[ind][0], int(self.__high_scores[
                ind][1])))
        # sort scores list in order to find the top three:
        new_scores.sort(key=lambda x:x[1], reverse=True)
        self.__high_scores = new_scores[0:3]
        self.update_score_board()

    def update_score_board(self):
        self.__hof_first.config(text=str(self.__high_scores[0][0] + "   Score: "
                                         + str(self.__high_scores[0][1])))
        self.__hof_second.config(text=str(self.__high_scores[1][0] + "   Score: "
                                          + str(self.__high_scores[1][1])))
        self.__hof_third.config(text=str(self.__high_scores[2][0] + "   Score: "
                                         + str(self.__high_scores[2][1])))

    def clear_text(self):
        self.__enter_name.delete('1.0', END)
        return

    def load_score_board(self):
        # load score file:
        with open("Resources/Data/score_board.txt", 'r') as file:
            high_scores = [tuple(line.split()) for line in file]
        return high_scores

    def save_high_scores(self):
        with open('Resources/Data/score_board.txt', 'w') as file:
            file.write('\n'.join('%s %s' % x for x in self.__high_scores))
