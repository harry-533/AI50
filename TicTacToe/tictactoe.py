"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    countX = 0
    countO = 0

    for i in board:
        for j in i:
            if j == X:
                countX += 1
            elif j == O:
                countO += 1

    if countX == countO:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()

    for i, row in enumerate(board):
        for j, value in enumerate(row):
            if value == EMPTY:
                possible_actions.add((i, j))
    
    return possible_actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if action not in actions(board):
        raise Exception("Invalid move")
    
    row, col = action
    board_copy = copy.deepcopy(board)
    board_copy[row][col] = player(board)
    return board_copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    columns = [[], [], []]

    for i in board:
        if i.count('X') == 3:
            return X
        elif i.count('O') == 3:
            return O
    
    for i in range(3):
        columns[i].append(board[0][i])
        columns[i].append(board[1][i])
        columns[i].append(board[2][i])
    
    for i in columns:
        if i.count('X') == 3:
            return X
        elif i.count('O') == 3:
            return O
        
    if board[0][0] == board[1][1] and board[1][1] == board[2][2]:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[1][1] == board[2][0]:
        return board[0][2]
    
    return None
        

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    empty_count = 0
    for i in board:
        empty_count += i.count(EMPTY)

    if winner(board) or empty_count == 0:
        return True

    return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def max_value(board):
    v = float('-inf')

    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = max(v, min_value(result(board, action)))

    return v


def min_value(board):
    v = float('inf')

    if terminal(board):
        return utility(board)
    
    for action in actions(board):
        v = min(v, max_value(result(board, action)))

    return v


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None
    
    if player(board) == X:
        plays = []
        for action in actions(board):
            plays.append([min_value(result(board, action)), action])

        return sorted(plays, key=lambda x: x[0], reverse=True)[0][1]  
    elif player(board) == O:
        plays = []
        for action in actions(board):
            plays.append([max_value(result(board, action)), action])

        return sorted(plays, key=lambda x: x[0])[0][1]