import boggle_board_randomizer as rand_helper
from gui_manager import *

GAME_TIME = 180  # in seconds


class Game:
    """
    Class responsible for the Boggle game logic: this class contains
    functions that check any valid/invalid word formations in the game,
    stores and controls data such as player score, player name, and current
    time of the game (which decreases as it progresses).
    """
    def __init__(self):
        self.__board = rand_helper.randomize_board()  # randomized board
        self.__score = 0  # initialize player score at 0
        self.__player_name = 'Empty'  # set to 'Empty' if no name is given
        self.__possible_words = self.load_words('boggle_dict.txt')
        self.__found_words = dict()  # will append all found words on board
        self.__time = GAME_TIME  # in seconds

    def get_board(self):
        return self.__board

    def get_score(self):
        return self.__score

    def get_player_name(self):
        return self.__player_name

    def increase_score(self, path):
        self.__score += path ** 2

    def decrease_time(self):
        self.__time -= 1
        return self.__time

    def load_words(self, file_path):
        # loads game words into a dictionary with value True
        word_dict = dict()
        with open(file_path) as f:
            for line in f.readlines():
                word_dict[line.strip('\n')] = True
            return word_dict

    def check_word(self, word, path):
        # check if word was already found:
        if word in self.__found_words:
            return -1  # unpress all the dice, don't add word to found words
        # check if word is in dictionary:
        if word in self.__possible_words:
            self.increase_score(path)
            # add to words found:
            self.__found_words[word] = True
            return True  # update words_found and word_var to empty string
        return False

    def convert_time(self, cur_time):
        # convert from seconds to minutes:seconds
        minutes = cur_time // 60
        seconds = cur_time - (60 * minutes)
        if seconds < 10:
            cur_time = "0" + str(minutes) + ':' + "0" + str(seconds)
        else:
            cur_time = "0" + str(minutes) + ':' + str(seconds)
        return cur_time

    def new_game(self):
        # resets game stats when called in order to start a fresh game
        self.__score = 0
        self.__board = rand_helper.randomize_board()
        self.__found_words = dict()
        self.__time = GAME_TIME

    def set_player_name(self, name):
        self.__player_name = name

