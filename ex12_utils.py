def is_in_bounds(board, coordinates):  # helper function
    """
    Checks if a coordinate is within board bounds.
    :param board:
    :param coordinates:
    :return: True if within bounds, False if not.
    """
    if not 0 <= coordinates[0] < len(board) or not 0 <= coordinates[1] < len(
            board[0]):
        return False
    return True


def get_word(board, path):  # helper function
    """
    Gets a path from the board and returns the word that is formed by the path.
    :param board: matrix - list of lists of strings
    :param path: list of tuples
    :return: string - word
    """
    word = str()
    for tup in path:
        row_ind = tup[0]
        col_ind = tup[1]
        letter = board[row_ind][col_ind]
        word += letter
    return word


def is_valid_path(board, path, words):  # 1
    """
    Checks if a path given is valid according to the game's rules and if so,
    gets the word formed by it.
    :param board: matrix - list of lists of strings
    :param path: list of tuples
    :param words: list/dict/set/some iterable container containing strings
    :return: string (formed word) if path was valid, None if it wasn't
    """
    # check if path is valid:
    valid = _is_valid(board, path)
    if valid:
        word = get_word(board, path)
        if word in words:
            return word
    else:  # word isn't in word list/path is not valid - return None:
        return


def _is_valid(board, path):
    """
    Checks if a given path is valid according to the game's rules.
    For a path that is valid: 1. each tuple appears only once on the list
                              2. the coordinates of the cells on the
                                 board must be consecutive, without skipping
                                 over a cell
                              3. all coordinates must be within board bounds
    :param board: matrix - list of lists of strings
    :param path: list of tuples
    :return: True if valid, False if not.
    """
    # check for repeating coordinates:
    tup_set = set(path)
    if len(tup_set) != len(path):
        return False  # path isn't valid!
    # check if path skips over any cells:
    for tup_ind in range(1, len(path)):
        if abs(path[tup_ind][0] - path[tup_ind - 1][0]) > 1 or \
                abs(path[tup_ind][1] - path[tup_ind - 1][1]) > 1:
            return False
    # check if all tuples are within board bounds:
    for tup in path:
        if not is_in_bounds(board, tup):
            return False
    return True  # valid - passed all checks!


def find_length_n_paths(n, board, words):  # 2
    """
    Goes recursively through the board and finds all possible paths of
    length n that form words from the collection given.
    :param n: int
    :param board: matrix - list of lists of strings
    :param words: list/dict/set/some iterable container containing strings
    :return: list of lists - each sublist contains tuples, for example:
             [[(0,0), (1,0), (2,0)], [(1,1), (1,2), (1,3)]]
    """
    # go through each cell in board and form the possible paths from it:
    path_list = list()
    for row_ind in range(len(board)):
        for col_ind in range(len(board[0])):
            _find_paths_helper(board, words, n, (row_ind, col_ind), str(),
                               list(), path_list)
    return path_list


def _find_paths_helper(board, words, n, cur_cell, word_so_far, steps_made,
                       path_list):
    # add current cell to list of path cells:
    steps_made.append(cur_cell)
    # add the string on this cell to the word being formed:
    word_so_far += board[cur_cell[0]][cur_cell[1]]
    if len(steps_made) == n:  # stopping condition - reached path with length n
        # check if word formed is really a word in the word list, if so -
        # return it's path:
        if word_so_far in words:
            print(word_so_far)
            path_list.append(steps_made)
        return

    movements_dict = get_possible_moves(cur_cell)
    for move in movements_dict:
        if is_in_bounds(board, movements_dict[move]) and \
                movements_dict[move] not in steps_made:
            # step is valid, step over to the next adjacent cell:
            _find_paths_helper(board, words, n, movements_dict[move],
                               word_so_far, steps_made.copy(), path_list)


def get_possible_moves(coordinates):
    """
    A dictionary of all 8 possible moves from a coordinate on the board.
    :param coordinates: tuple with the location on the x and y axis, like (2,3)
    :return: dictionary where the key is the movement direction, and the
             value is the new coordinate according to that move
    """
    possible_moves = {'up': (coordinates[0] - 1, coordinates[1]),
                      'up right': (coordinates[0] - 1, coordinates[1] + 1),
                      'right': (coordinates[0], coordinates[1] + 1),
                      'down right': (coordinates[0] + 1, coordinates[1] + 1),
                      'down': (coordinates[0] + 1, coordinates[1]),
                      'down left': (coordinates[0] + 1, coordinates[1] - 1),
                      'left': (coordinates[0], coordinates[1] - 1),
                      'up left': (coordinates[0] - 1, coordinates[1] - 1)}
    return possible_moves


def find_length_n_words(n, board, words):
    """
    Goes recursively through the board and finds all possible paths that
    form words of length n from the collection given.
    :param n: int
    :param board: matrix - list of lists of strings
    :param words: list/dict/set/some iterable container containing strings
    :return: list of lists - each sublist contains tuples, for example:
             [[(0,0), (1,0), (2,0)], [(1,1), (1,2), (1,3)]]
    """
    # go through each cell in board and form the possible paths from it:
    all_paths = dict()  # {word: [paths]}
    for row_ind in range(len(board)):
        for col_ind in range(len(board[0])):
            _find_words_helper(board, words, n, (row_ind, col_ind), str(),
                               list(), all_paths)
    # convert dict to list:
    res = []
    for val in all_paths.values():
        for path in val:
            res.append(path)
    return res


def _find_words_helper(board, words, n, cur_cell, word_so_far, steps_made,
                       all_paths, max_score=False):
    # add current cell to list of path cells:
    steps_made.append(cur_cell)
    # add the string on this cell to the word being formed:
    word_so_far += board[cur_cell[0]][cur_cell[1]]
    if len(word_so_far) > n:
        return  # word is too long - not a valid path
    if len(word_so_far) == n:  # reached a full word
        if word_so_far in words:  # found a word
            if not max_score:
                if word_so_far in all_paths:
                    all_paths[word_so_far].append(steps_made)
                else:
                    all_paths[word_so_far] = [steps_made]

            if max_score:
                if word_so_far not in all_paths or \
                        len(steps_made) > len(all_paths[word_so_far]):
                    all_paths[word_so_far] = steps_made
        return

    movements_dict = get_possible_moves(cur_cell)
    for move in movements_dict:
        if is_in_bounds(board, movements_dict[move]) and \
                movements_dict[move] not in steps_made:
            # step is valid, step over to the next adjacent cell:
            _find_words_helper(board, words, n, movements_dict[move],
                               word_so_far, steps_made.copy(), all_paths,
                               max_score)


def max_score_paths(board, words):
    """
    Finds the path on the board that gives the highest score for each word
    in words, and stores them all in a list.
    :param board: matrix - list of lists of strings
    :param words: list/dict/set/some iterable container containing strings
    :return: list of lists - each sublist contains tuples, for example:
             [[(3,2)], [(0,0), (1,0), (2,0)], [(1,1), (1,2)], ...]
    """
    # create a set that stores all lengths of words given:
    all_lengths = set()
    for word in words:
        all_lengths.add(len(word))
    # call the recursive func with a different n each time to get all words:
    word_dict = dict()
    for n in all_lengths:
        for row_ind in range(len(board)):
            for col_ind in range(len(board[0])):
                _find_words_helper(board, words, n, (row_ind, col_ind),
                                   str(), list(), word_dict, True)

    # arrange all the paths found in a list:
    maximum_paths = list()
    for word in word_dict:
        max_path = word_dict[word]
        maximum_paths.append(max_path)
    return maximum_paths
