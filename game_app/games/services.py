"""
Game logic services for FizzBuzz and TicTacToe games.
"""


def fizzbuzz_logic(number):
    """
    Determine the correct FizzBuzz answer for a given number.
    
    Args:
        number (int): The number to evaluate
    
    Returns:
        str: The correct answer ('FIZZBUZZ', 'FIZZ', 'BUZZ', or the number as string)
    """
    if number % 15 == 0:
        return 'FIZZBUZZ'
    elif number % 3 == 0:
        return 'FIZZ'
    elif number % 5 == 0:
        return 'BUZZ'
    else:
        return str(number)


def validate_fizzbuzz_answer(number, user_answer):
    """
    Validate if the user's answer is correct for the given number.
    
    Args:
        number (int): The current number
        user_answer (str): The user's answer
    
    Returns:
        bool: True if correct, False otherwise
    """
    correct_answer = fizzbuzz_logic(number)
    return user_answer.strip().upper() == correct_answer.upper()


def initialize_tictactoe_board():
    """
    Initialize an empty TicTacToe board.
    
    Returns:
        list: A 3x3 board represented as a list of 9 elements
    """
    return ['' for _ in range(9)]


def check_winner(board):
    """
    Check if there's a winner on the TicTacToe board.
    
    Args:
        board (list): The current board state
    
    Returns:
        str or None: 'X' if X wins, 'O' if O wins, 'Draw' if board is full, None otherwise
    """
    # Winning combinations
    win_patterns = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]               # Diagonals
    ]
    
    # Check for winner
    for pattern in win_patterns:
        if board[pattern[0]] == board[pattern[1]] == board[pattern[2]] != '':
            return board[pattern[0]]
    
    # Check for draw
    if '' not in board:
        return 'Draw'
    
    return None


def get_available_moves(board):
    """
    Get all available positions on the board.
    
    Args:
        board (list): The current board state
    
    Returns:
        list: List of available position indices
    """
    return [i for i, cell in enumerate(board) if cell == '']


def _minimax(board, is_maximizing):
    """
    Evaluate board positions with minimax.

    Returns:
        int: score from O (computer) perspective.
    """
    result = check_winner(board)
    if result == 'O':
        return 1
    if result == 'X':
        return -1
    if result == 'Draw':
        return 0

    if is_maximizing:
        best_score = -10
        for move in get_available_moves(board):
            board[move] = 'O'
            score = _minimax(board, False)
            board[move] = ''
            if score > best_score:
                best_score = score
        return best_score

    best_score = 10
    for move in get_available_moves(board):
        board[move] = 'X'
        score = _minimax(board, True)
        board[move] = ''
        if score < best_score:
            best_score = score
    return best_score


def tictactoe_move(board):
    """
    Choose the best move for the computer (O) using minimax.

    Args:
        board (list): The current board state

    Returns:
        int or None: Best position for computer move, or None if no moves available
    """
    available = get_available_moves(board)
    if not available:
        return None

    best_score = -10
    best_move = available[0]

    for move in available:
        board[move] = 'O'
        score = _minimax(board, False)
        board[move] = ''
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def is_valid_move(board, position):
    """
    Check if a move is valid.
    
    Args:
        board (list): The current board state
        position (int): The position to check
    
    Returns:
        bool: True if valid, False otherwise
    """
    return 0 <= position < 9 and board[position] == ''
