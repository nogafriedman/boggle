from tkinter import *
from tkinter import messagebox
from main_menu import *
from game_logic import *
from dice import *
from board import *
import boggle_board_randomizer as rand_helper

from main_menu import MainMenu

MAIN_TITLE = 'Boggle'
MAIN_MENU = "Main Menu"
TITLE_FONT = ("Helvetica", 36, "bold")
RIGHT_FONT_TITLE = ("Helvetica", 12, "bold")
RIGHT_FONT = ("Helvetica", 12)

class GUIManager:
    """
    This class deals with the visual GUI elements of the game. It contains
    the frames constructing the game window, labels and other tkinter
    objects. It also changes according to the progress of the game (rotates
    between the main menu and the gameplay window, updates labels on the
    board, etc).
    """
    def __init__(self, game_obj):
        # Gameplay fields (from Game/Boggle object):
        self.__game = game_obj
        self.__str_board = game_obj.get_board()
        self.__score = game_obj.get_score()
        self.__root = self.create_window()
        # main menu:
        self.__main_menu = MainMenu(self.__root, self, self.__game)
        self.__main_menu.frame.pack()
        # main gameplay frame:
        self.__gameplay_frame = Frame(self.__root, height=500, width=750,
                                      bg="white")
        # gameplay sub frames:
        self.__game_title_frame = self.top_title_frame()
        self.__exit_button = Button(self.__gameplay_frame, height=50, width=50,
                                    image=self.__main_menu.exit_image,
                                    bg="white", command=self.return_to_menu)
        # right frame - divided into 3 parts (upper, middle, bottom):
        self.__right_frame, upper_widgets, middle_widget, bottom_widgets = \
            self.main_right_frame()
        self.__board = Board(self.__gameplay_frame, self.__str_board)
        self.__board_frame = self.__board.get_board_frame()
        # GUI & widgets fields:
        self.__timer_label = upper_widgets[1]
        self.__timer_var = upper_widgets[2]
        self.__score_var = upper_widgets[3]
        self.__word_var = upper_widgets[4]
        self.__words_found_var = bottom_widgets[1]
        self.__board.set_word_var(self.__word_var)
        # main menu frames:
        self.present_gameplay_sub_frames()
        self.__is_active = False  # True if game/timer is currently running
        self.__root.mainloop()

    def create_window(self):
        root = Tk()
        root.minsize(750, 500)
        root.config(bg="white")
        root.title(MAIN_TITLE)
        return root

    def present_gameplay_sub_frames(self):
        self.__exit_button.place(x=600, y=6)
        self.__game_title_frame.pack(side=TOP, fill=X)
        self.__right_frame.pack(side=RIGHT, expand=True)
        self.__board_frame.pack(side=LEFT)

    def top_title_frame(self):
        frame = Frame(self.__gameplay_frame, height=70, width=700, bg="white",
                      highlightbackground="light blue",
                      highlightthickness=2)
        label = Label(frame, text=MAIN_TITLE, font=TITLE_FONT, bg="white")
        label.grid(padx=200, pady=0)
        return frame

    def main_right_frame(self):
        frame = Frame(self.__gameplay_frame, width=700, height=300, bg="white",
                      highlightbackground="light blue",
                      highlightthickness=2)
        upper_widgets = self.upper_right_frame(frame)
        message_var = upper_widgets[5]
        message = upper_widgets[6]
        score_var = upper_widgets[3]
        bottom_widgets = self.bottom_right_frame(frame)
        words_found_var = bottom_widgets[1]
        middle_widget = self.middle_check_frame(frame, message_var, message,
                                                words_found_var, score_var)
        upper_widgets[0].pack()
        middle_widget.pack(fill=X)
        bottom_widgets[0].pack(side= TOP)
        return [frame, upper_widgets, middle_widget, bottom_widgets]

    def upper_right_frame(self, main_frame):
        # contains timer, score, current word
        frame = Frame(main_frame, bg="white")
        # timer:
        timer_title = Label(frame, bg="white", text="Timer",
                            font=RIGHT_FONT_TITLE, width=30)
        timer_title.grid(padx=0, pady=3)
        timer_var = StringVar()
        timer_var.set('03:00')
        timer_label = Label(frame, bg="white", textvariable=timer_var,
                            font=RIGHT_FONT)
        timer_label.grid(padx=0, pady=6)
        # score:
        score_title = Label(frame, bg="white", text="Current Score",
                            font=RIGHT_FONT_TITLE)
        score_title.grid(padx=5, pady=3)
        score_var = StringVar()
        score_var.set('0')
        score_label = Label(frame, bg="white", textvariable=score_var,
                            font=RIGHT_FONT)
        score_label.grid(padx=5, pady=6)
        # word so far:
        cur_word = Label(frame, bg="white", text="Current Word", height=5,
                         font=RIGHT_FONT_TITLE)
        cur_word.grid(padx=3, pady=0)
        word_var = StringVar()
        word_var.set(str())
        word_label = Label(frame, bg="white", textvariable=word_var,
                           font=(RIGHT_FONT, 20))
        word_label.grid(padx=0, pady=0)
        # message to player - if word they formed is invalid/has been found:
        message_var = StringVar()
        message_var.set(str())
        message = Label(frame, bg="white", textvariable=message_var,
                        font=("Arial", 10))
        message.grid(padx=0, pady=0)
        return [frame, timer_label, timer_var, score_var,  word_var,
                message_var, message]

    def bottom_right_frame(self, main_frame):
        # words found:
        frame = Frame(main_frame, bg="white")
        words_found_title = Label(frame, bg="white", text="Words Found",
                                  font=RIGHT_FONT_TITLE)
        words_found_title.grid(padx=0, pady=15)
        mini_frame = Frame(frame, width=100, height=30, bg="white",
                           highlightbackground="white", highlightthickness=1)
        mini_frame.grid(padx=0, pady=10)
        words_found_var = StringVar()
        words_found_var.set(str())
        words_found_label = Label(mini_frame,
                                  bg="white", textvariable=words_found_var,
                                  font=("Arial", 10))
        words_found_label.grid(padx=0, pady=6)
        return [frame, words_found_var]

    def middle_check_frame(self, main_frame, message_var, message,
                           words_found_var, score_var):
        frame = Frame(main_frame, bg="white")
        reset_word = Button(frame, width=6, height=2, text="Reset\nWord",
                            font=("Tahoma", 20),
                            command=lambda: self.reset_word())
        dummy1 = Label(frame, width=4, height=10, bg="white").pack(side=RIGHT)
        reset_word.pack(side=RIGHT)
        check_word = Button(frame, width=6, height=2, text="Check\nWord",
                            font=("Tahoma", 20), bg="light blue",
                            command=lambda: self.check_word(message_var, message,
                                                            words_found_var,
                                                            score_var))
        dummy2 = Label(frame, width=4, height=10, bg="white").pack(side=LEFT)
        check_word.pack(side=LEFT)
        return frame

    def check_word(self, message_var, message, words_found_var, score_var):
        word = self.__board.get_word_var().get()
        path = self.__board.get_path()
        val = self.__game.check_word(word, len(path))
        if not val:  # word not in dictionary
            message_var.set("Invalid word! Try again.")
            message.after(3000, self.reset_message, message_var)
        if val == -1:  # word has already been found by player
            message_var.set("Already found!")
            message.after(3000, self.reset_message, message_var)
        elif val:  # found a valid word!
            message_var.set("Correct!")
            message.after(3000, self.reset_message, message_var)
            # add word to words found:
            words_str = words_found_var.get()
            if words_str is not str():  # if it's not the first word
                words_found_var.set(words_str + ', ' + word)
            else:
                words_found_var.set(word)
            new_score = self.__game.get_score()
            score_var.set(new_score)
        # do in all cases:
        self.reset_word()

    def reset_word(self):
        # resets pressed buttons, path and word_so_far after word check:
        for dice in self.__board.get_path():
            dice.set_state(False)  # unpress all buttons
        self.__board.set_path(list())  # reset path list
        self.__board.set_last_pressed(tuple())  # reset last pressed coordinates
        self.__board.get_word_var().set(str())  # reset word_so_far

    def timer(self, timer_label, timer_var):
        if not self.__is_active:  # if game is not active timer stays paused
            return
        cur_time = self.__game.decrease_time()  # cur_time = int (seconds)
        if cur_time < 0:
            return  # makes sure that the timer stops at 00:00
        timer_label.after(1000, self.timer, timer_label, timer_var)
        time_str = self.__game.convert_time(cur_time)
        timer_var.set(time_str)
        if cur_time == 0:
            self.game_over()

    def reset_message(self, message_var):
        # resets the message about found word for the player after 3 seconds
        message_var.set(str())

    def start_game(self):
        self.__main_menu.frame.forget()
        self.__gameplay_frame.pack(fill=BOTH)
        self.__is_active = True
        self.timer(self.__timer_label, self.__timer_var)

    def return_to_menu(self):
        self.reset_word()
        self.__gameplay_frame.forget()
        self.reset_stats()
        self.new_board()
        self.__is_active = False
        self.start_main_menu()

    def new_board(self):
        self.__str_board = self.__game.get_board()
        self.__board.reset_board(self.__str_board)

    def start_main_menu(self):
        self.__main_menu.clear_text()
        self.__main_menu.frame.pack()
        return

    def game_over(self):
        self.__main_menu.update_score(self.__game.get_player_name(),
                                      self.__game.get_score())
        self.__main_menu.save_high_scores()  # save high scores to file
        msgbox = messagebox.askquestion(title="GAME OVER",
                                        message="Time's up!\nYour final score is: " +
                                                str(self.__score_var.get()) + "\n" +
                                                "Play another game?")
        if msgbox == 'no':
            # go back to main menu:
            self.__is_active = False
            self.return_to_menu()
        if msgbox == 'yes':
            self.__is_active = True
        self.reset_stats()  # resets all stats
        self.reset_board()  # randomizes new board
        self.timer(self.__timer_label, self.__timer_var)  # countdown will
        # only begin if is_active is True (only if player picked yes)

    def reset_stats(self):
        # resets game stats after user finished playing.
        self.reset_word()
        # reset pressed dice, path, word_var:
        self.__words_found_var.set(str())  # reset found words
        self.__score_var.set("0")  # reset score
        self.__timer_var.set("03:00")
        # reset stats in game_logic:
        self.__game.new_game()

    def reset_board(self):
        # randomize new board (when starting a new game after playing):
        self.__str_board = self.__game.get_board()
        self.__board.initiate_dice(self.__str_board)
