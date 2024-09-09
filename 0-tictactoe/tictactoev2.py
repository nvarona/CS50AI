import math

X = "X"
O = "O"
EMPTY = None

def initial_state():
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return O if x_count > o_count else X

def actions(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == EMPTY]

def result(board, action):
    new_board = [row[:] for row in board]  # Create a deep copy
    i, j = action
    new_board[i][j] = player(board)
    return new_board

def winner(board):
    # Check rows, columns and diagonals
    for player in (X, O):
        # Rows and columns
        for i in range(3):
            if all(board[i][j] == player for j in range(3)) or \
               all(board[j][i] == player for j in range(3)):
                return player
        # Diagonals
        if all(board[i][i] == player for i in range(3)) or \
           all(board[i][2-i] == player for i in range(3)):
            return player
    return None

def terminal(board):
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)

def utility(board):
    winner_player = winner(board)
    if winner_player == X:
        return 1
    elif winner_player == O:
        return -1
    else:
        return 0

def minimax(board):
    def max_value(board):
        if terminal(board):
            return utility(board)
        v = float('-inf')
        for action in actions(board):
            v = max(v, min_value(result(board, action)))
        return v

    def min_value(board):
        if terminal(board):
            return utility(board)
        v = float('inf')
        for action in actions(board):
            v = min(v, max_value(result(board, action)))
        return v

    current_player = player(board)
    if current_player == X:
        return max(actions(board), key=lambda a: min_value(result(board, a)))
    else:
        return min(actions(board), key=lambda a: max_value(result(board, a)))
