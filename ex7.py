

import random

# --- Constants ---

# Board Dimensions Limits
MIN_DIM = 2
MAX_DIM = 100

# Tic Tac Toe Constants
TTT_SIZE = 3
TTT_MAX_CELLS = 9
TTT_CELL_MIN = 1

# Connect N Sequence Logic Thresholds
SEQ_LEN_2 = 2
SEQ_LEN_3 = 3
SEQ_LEN_4 = 4
SEQ_LEN_5 = 5

THRESHOLD_SMALL_MIN = 4
THRESHOLD_SMALL_MAX = 5
THRESHOLD_MEDIUM_MIN = 6
THRESHOLD_MEDIUM_MAX = 10

# Tokens
EMPTY = '.'
TOKEN_P1 = 'X'
TOKEN_P2 = 'O'

# Player Identification
PLAYER_1 = 1
PLAYER_2 = 2

# Player Types (Internal Representation)
HUMAN = 1
RANDOM_COMPUTER = 2
STRATEGIC_COMPUTER = 3

# Player Input Choices
INPUT_HUMAN = 'h'
INPUT_RANDOM = 'r'
INPUT_STRATEGIC = 's'

# Game Modes
MODE_CONNECT_N = 1
MODE_TIC_TAC_TOE = 2

# Return Codes / Indices
INVALID_INDEX = -1
NOT_FOUND = -1
FIRST_COLUMN_INDEX = 0

def main():
    """
    Main function to run the Upgraded Connect-4 (Connect-N) game.
    """
    
    # 1. Get Board Dimensions
    rows, cols = get_board_dimensions()
    
    # 2. Determine Game Logic
    game_mode, connect_n, final_rows, final_cols = determine_game_rules(rows, cols)
    
    # 3. Initialize Board
    board = create_board(final_rows, final_cols)
    
    # 4. Handle Game Modes
    if game_mode == MODE_TIC_TAC_TOE:
        print("Tic Tac Toe (Human vs Human)")
        print() 
        run_tic_tac_toe(board)
    else:
        print(f"Connect Four - Or More [Or Less] ({final_rows} rows x {final_cols} cols, connect {connect_n})")
        print()
        
        p1_type = get_player_type(PLAYER_1)
        p2_type = get_player_type(PLAYER_2)
        
        run_connect_n(board, final_rows, final_cols, connect_n, p1_type, p2_type)


def get_board_dimensions():
    """
    Asks the user for rows and columns.
    """
    while True:
        try:
            print("Enter number of rows")
            rows_input = input()
            print("Enter number of columns")
            cols_input = input()
            
            rows = int(rows_input)
            cols = int(cols_input)
            
            if rows < MIN_DIM or rows > MAX_DIM or cols < MIN_DIM or cols > MAX_DIM:
                print(f"Dimensions must be between {MIN_DIM} and {MAX_DIM}.")
                continue
                
            return rows, cols
            
        except ValueError:
            print("Invalid input. Please enter integers.")


def determine_game_rules(rows, cols):
    """
    Determines the game mode and winning sequence length.
    Returns: (game_mode, connect_n, final_rows, final_cols)
    """
    # Rule: If 2 is chosen for either -> Sequence is 2
    if rows == MIN_DIM or cols == MIN_DIM:
        return MODE_CONNECT_N, SEQ_LEN_2, rows, cols
    
    # Rule: If either is 3 -> Tic-Tac-Toe (3x3 fixed)
    if rows == TTT_SIZE or cols == TTT_SIZE:
        return MODE_TIC_TAC_TOE, SEQ_LEN_3, TTT_SIZE, TTT_SIZE
    
    # Connect-N Logic for other sizes
    max_dim = max(rows, cols)
    
    if THRESHOLD_SMALL_MIN <= max_dim <= THRESHOLD_SMALL_MAX:
        return MODE_CONNECT_N, SEQ_LEN_3, rows, cols
    elif THRESHOLD_MEDIUM_MIN <= max_dim <= THRESHOLD_MEDIUM_MAX:
        return MODE_CONNECT_N, SEQ_LEN_4, rows, cols
    else:
        return MODE_CONNECT_N, SEQ_LEN_5, rows, cols


def create_board(rows, cols):
    """Initializes the game board with empty tokens."""
    return [[EMPTY for _ in range(cols)] for _ in range(rows)]


def get_player_type(player_number):
    """Asks user for player type using input() to keep cursor on same line."""
    while True:
        prompt = f"Choose type for player {player_number}: {INPUT_HUMAN} - human, {INPUT_RANDOM} - random/simple computer, {INPUT_STRATEGIC} - strategic computer: "
        choice = input(prompt)
        
        if choice.lower() == INPUT_HUMAN:
            return HUMAN
        elif choice.lower() == INPUT_RANDOM:
            return RANDOM_COMPUTER
        elif choice.lower() == INPUT_STRATEGIC:
            return STRATEGIC_COMPUTER
        else:
            print(f"Invalid selection. Enter {INPUT_HUMAN}, {INPUT_RANDOM} or {INPUT_STRATEGIC}.")


def print_connect_n_board(board, rows, cols):
    """Prints the Connect-N board."""
    for r in range(rows):
        line = "|"
        for c in range(cols):
            line += f"{board[r][c]}|"
        print(line)
    
    number_line = ""
    for c in range(1, cols + 1):
        number_line += f" {c % 10}"
    print(number_line)
    print() 


# ---------------------------------------------------------------------------
# Connect-N Implementation
# ---------------------------------------------------------------------------

def run_connect_n(board, rows, cols, connect_n, p1_type, p2_type):
    """Main game loop for Connect-N mode."""
    print_connect_n_board(board, rows, cols)
    
    if is_board_full(board, rows, cols):
        print("Board full and no winner. It's a tie!")
        return

    is_game_over = False
    turn_counter = 0 
    
    while not is_game_over:
        # Determine current player
        if turn_counter % 2 == 0:
            current_player = PLAYER_1
            current_token = TOKEN_P1
            current_type = p1_type
            opponent_token = TOKEN_P2
        else:
            current_player = PLAYER_2
            current_token = TOKEN_P2
            current_type = p2_type
            opponent_token = TOKEN_P1
            
        is_game_over = act_player_turn(board, rows, cols, connect_n, 
                                       current_type, current_player, 
                                       current_token, opponent_token)
        
        if not is_game_over:
            turn_counter += 1


def act_player_turn(board, rows, cols, connect_n, player_type, player_num, player_token, opponent_token):
    """Executes a single turn."""
    chosen_col = INVALID_INDEX
    
    print(f"Player {player_num} ({player_token}) turn.")
    
    if player_type == HUMAN:
        chosen_col = human_choose(board, rows, cols)
    elif player_type == RANDOM_COMPUTER:
        chosen_col = random_computer_choose(board, rows, cols)
        print(f"Computer chose column {chosen_col + 1}")
    else: # STRATEGIC_COMPUTER
        chosen_col = strategic_computer_choose(board, rows, cols, connect_n, player_token, opponent_token)
        print(f"Computer chose column {chosen_col + 1}")
    
    make_move(board, rows, chosen_col, player_token)
    print_connect_n_board(board, rows, cols)
    
    if check_victory_length(board, rows, cols, connect_n, player_token):
        print(f"Player {player_num} ({player_token}) wins!")
        return True
    
    if is_board_full(board, rows, cols):
        print("Board full and no winner. It's a tie!")
        return True
        
    return False


def human_choose(board, rows, cols):
    """Handles human input validation for column selection."""
    while True:
        user_input = input(f"Enter column (1-{cols}): ")
        
        if not user_input.strip() or not is_integer(user_input):
            print("Invalid input. Enter a number.")
            continue
            
        col = int(user_input)
        
        if col < 1 or col > cols:
            print(f"Invalid column. Choose between 1 and {cols}.")
            continue
            
        if is_column_full(board, col - 1):
            print(f"Column {col} is full. Choose another column.")
            continue
            
        return col - 1


def random_computer_choose(board, rows, cols):
    """Picks a random valid column."""
    valid_cols = []
    for c in range(cols):
        if not is_column_full(board, c):
            valid_cols.append(c)
    return random.choice(valid_cols)


def strategic_computer_choose(board, rows, cols, connect_n, player_token, opponent_token):
    """
    Strategic logic: Win -> Block -> Sequence -> Block Sequence -> Arbitrary
    """
    # Scan for potential sequences from length 1 up to N-2
    # Logic: If N=4, we check for 3 tokens (N-1), then 2 tokens (N-2)
    min_sequence_check = 1
    max_sequence_check = connect_n - 1
    
    for i in range(min_sequence_check, max_sequence_check): 
        step_amount = i
        
        # 1. Try to win (Player)
        move = check_steps_before_can_happen(board, rows, cols, connect_n, step_amount, player_token)
        if move != NOT_FOUND: return move
        
        # 2. Block (Opponent)
        move = check_steps_before_can_happen(board, rows, cols, connect_n, step_amount, opponent_token)
        if move != NOT_FOUND: return move

    # Priority 5: Arbitrary rule
    return possible_computer_move(board, rows, cols)


def check_steps_before_can_happen(board, rows, cols, connect_n, steps_missing, token):
    """Checks if placing a token completes a sequence of wanted length."""
    wanted_length = connect_n - steps_missing
    best_col = NOT_FOUND
    min_dist_middle = cols + 1
    
    for c in range(cols):
        r = get_free_row(board, rows, c)
        if r == INVALID_INDEX: continue
        
        board[r][c] = token
        
        if check_victory_length(board, rows, cols, wanted_length, token):
            dist = distance_from_middle(cols, c)
            if best_col == NOT_FOUND or dist < min_dist_middle:
                best_col = c
                min_dist_middle = dist
        
        board[r][c] = EMPTY # Undo
        
    return best_col


def possible_computer_move(board, rows, cols):
    """Selects a valid column closest to the center."""
    best_col = NOT_FOUND
    min_dist_middle = cols + 1
    
    for c in range(cols):
        if not is_column_full(board, c):
            dist = distance_from_middle(cols, c)
            if dist < min_dist_middle:
                min_dist_middle = dist
                best_col = c
    return best_col


def distance_from_middle(cols, col_idx):
    """Calculates distance from center."""
    val = 2 * col_idx - (cols - 1)
    return abs(val)


def make_move(board, rows, col, token):
    """Places a token in the lowest available row."""
    r = get_free_row(board, rows, col)
    if r != INVALID_INDEX:
        board[r][col] = token
        return True
    return False


def get_free_row(board, rows, col):
    """Returns the index of the first empty row from bottom."""
    for r in range(rows - 1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return INVALID_INDEX


def is_column_full(board, col):
    return board[FIRST_COLUMN_INDEX][col] != EMPTY


def is_board_full(board, rows, cols):
    for c in range(cols):
        if not is_column_full(board, c):
            return False
    return True


def check_victory_length(board, rows, cols, length, token):
    """Checks for a sequence of 'length' for 'token'."""
    # Vertical
    for c in range(cols):
        count = 0
        for r in range(rows):
            if board[r][c] == token:
                count += 1
                if count == length: return True
            else:
                count = 0
    # Horizontal
    for r in range(rows):
        count = 0
        for c in range(cols):
            if board[r][c] == token:
                count += 1
                if count == length: return True
            else:
                count = 0
    # Diagonal
    for r in range(rows):
        for c in range(cols):
            if r + length <= rows and c + length <= cols:
                match = True
                for i in range(length):
                    if board[r+i][c+i] != token:
                        match = False; break
                if match: return True
    # Reverse Diagonal
    for r in range(rows):
        for c in range(cols):
            if r + length <= rows and c - length + 1 >= 0:
                match = True
                for i in range(length):
                    if board[r+i][c-i] != token:
                        match = False; break
                if match: return True
    return False

# ---------------------------------------------------------------------------
# Tic-Tac-Toe Implementation
# ---------------------------------------------------------------------------

def run_tic_tac_toe(board):
    """Special game loop for Tic-Tac-Toe mode."""
    print_tic_tac_toe_board(board)
    print() 
    
    is_game_over = False
    turn_counter = 0 
    
    while not is_game_over and turn_counter < TTT_MAX_CELLS:
        player_num = PLAYER_1 if turn_counter % 2 == 0 else PLAYER_2
        token = TOKEN_P1 if player_num == PLAYER_1 else TOKEN_P2
        
        # Get Move
        cell = INVALID_INDEX
        while True:
            user_input = input(f"Enter position ({TTT_CELL_MIN}-{TTT_MAX_CELLS}): ")
            
            if not user_input.strip():
                continue

            if not is_integer(user_input):
                print("Invalid input. Enter a number.")
                continue
                
            cell = int(user_input)
            if cell < TTT_CELL_MIN or cell > TTT_MAX_CELLS:
                print(f"Invalid position. Choose between {TTT_CELL_MIN} and {TTT_MAX_CELLS}.")
                continue
            
            # Convert 1-9 to row/col (0-2)
            # cell-1 handles 0-indexing
            row = (cell - 1) // TTT_SIZE
            col = (cell - 1) % TTT_SIZE
            
            if board[row][col] != EMPTY:
                print("Position is taken. Choose another.")
                continue
                
            break
        
        row = (cell - 1) // TTT_SIZE
        col = (cell - 1) % TTT_SIZE
        board[row][col] = token
        
        print()
        print_tic_tac_toe_board(board)
        print()
        
        if check_victory_length(board, TTT_SIZE, TTT_SIZE, TTT_SIZE, token):
            print(f"Player {player_num} ({token}) wins!")
            return
            
        turn_counter += 1

    print("It's a tie!")


def print_tic_tac_toe_board(board):
    """Prints board with dots for empty cells."""
    for r in range(TTT_SIZE):
        line = "|"
        for c in range(TTT_SIZE):
            line += f"{board[r][c]}|"
        print(line)


def is_integer(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

if __name__ == "__main__":
    main()