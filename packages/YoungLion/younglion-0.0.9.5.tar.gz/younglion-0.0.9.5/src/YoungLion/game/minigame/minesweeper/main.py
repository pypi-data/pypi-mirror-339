import .custom
number_colors = {
    1: "\033[34m", 
    2: "\033[32m", 
    3: "\033[31m", 
    4: "\033[35m", 
    5: "\033[36m", 
    6: "\033[91m",
    7: "\033[33m", 
    8: "\033[90m",  
}
def GameMapStr(board: custom.MinesweeperMap, last_move: tuple[int, int] = None) -> str:
    """
    Returns a string representation of the board with coordinate labels and colorized output.
    - Hidden cells are shown as filled green squares.
    - Revealed mines are shown in red.
    - Revealed numbers are color-coded.
    - The row and column labels corresponding to last_move are highlighted with a yellow background.
    """
    cell_width = 2
    header_cells = []
    for col in range(board.cols):
        col_str = f"{col:>{cell_width}}"
        if last_move and col == last_move[1]:
            col_str = f"\033[43m{col_str}\033[0m"  
        header_cells.append(col_str)
    header = "   " + "".join(header_cells)
    rows_str = [header]
    for i, row in enumerate(board.grid):
        row_label = f"{i:>{cell_width}}"
        if last_move and i == last_move[0]:
            row_label = f"\033[43m{row_label}\033[0m"

        row_cells = []
        for j, (value, visible) in enumerate(row):
            if not visible:
                cell_str = "\033[32m■\033[0m"  
            else:
                if value == -1:
                    cell_str = "\033[31m*\033[0m" 
                elif value == 0:
                    cell_str = "\033[39m■\033[0m"
                else:
                    color = number_colors.get(value, "\033[37m")
                    cell_str = f"{color}{value}\033[0m"
            row_cells.append(cell_str.center(cell_width))
        rows_str.append(f"{row_label} | " + " ".join(row_cells))
    return "\n".join(rows_str)
def print_help():
    help_text = """
\033[1;36mGame Instructions:\033[0m

- Enter your move as two integers separated by a space.
  These numbers represent the row and column of the cell to reveal.
  For example: "3 4" reveals the cell at row 3, column 4.
  
- Board Coordinates:
    - The top header shows column numbers.
    - The left side shows row numbers.
    - The coordinate labels for your last move are highlighted in yellow.
  
- Symbols:
    - \033[32m■\033[0m: Hidden cell.
    - \033[31m*\033[0m: Revealed mine.
    - (empty): Revealed safe cell (0 adjacent mines).
    - Colored numbers: Revealed cell with adjacent mine count.
  
- Commands:
    - Type \033[1;35mhelp\033[0m to see these instructions.
    - Type \033[1;35mexit\033[0m or \033[1;35mquit\033[0m to exit at any prompt.
    - When the game ends, press Enter (with no input) to start a new game.
"""
    print(help_text)
def init_game():
    while True:
        try:
            dims = input("\033[1;35mEnter board dimensions (rows cols): \033[0m").strip()
            if dims.lower() in ("exit", "quit"):
                exit(0)
            rows, cols = map(int, dims.split())
            break
        except Exception as e:
            print(f"\033[31mInvalid dimensions input: {e}. Please try again.\033[0m")
    while True:
        try:
            mines = input("\033[1;35mEnter number of mines: \033[0m").strip()
            if mines.lower() in ("exit", "quit"):
                exit(0)
            mines_count = int(mines)
            break
        except Exception as e:
            print(f"\033[31mInvalid mine count: {e}. Please try again.\033[0m")
    max_neighbors_input = input("\033[1;35mEnter max neighbors allowed for a new mine (default 5): \033[0m").strip()
    if max_neighbors_input == "" or not max_neighbors_input.isdigit():
        max_neighbors = 5
    else:
        max_neighbors = int(max_neighbors_input)
    return custom.CustomMinesweeper((rows, cols), mines_count, max_neighbors)
def init():
    while True:
        game = init_game()
        last_move = None
        while True:
            print("\033[2J\033[f\033[0m", end="")
            if game.status == custom.MinesweeperGameStatus.starting:
                print("\033[33;1mThe Game is on!\033[0m")
            elif game.status == custom.MinesweeperGameStatus.continue_:
                print("\033[32;1mGame continues. Think about your next move.\033[0m")
            elif game.status == custom.MinesweeperGameStatus.win:
                print("\033[32;1mCongratulations, you won!\033[0m")
                print(GameMapStr(game.game_map, last_move))
                break
            elif game.status == custom.MinesweeperGameStatus.lose:
                print("\033[31;1mGame Over. You hit a mine.\033[0m")
                print(GameMapStr(game.game_map, last_move))
                break
            print(GameMapStr(game.game_map, last_move))
            user_input = input("\033[1;35mEnter move (row col) or type 'help': \033[0m").strip()
            if user_input.lower() == "help":
                print_help()
                input("Press Enter to continue...")
                continue
            if user_input.lower() in ("exit", "quit"):
                exit(0)
            try:
                parts = user_input.split()
                if len(parts) != 2:
                    raise ValueError("You must enter exactly two numbers separated by a space.")
                x, y = map(int, parts)
            except Exception as e:
                print(f"\033[31mInvalid input: {e}. Please try again.\033[0m")
                input("Press Enter to continue...")
                continue
            last_move = (x, y)
            game.make_move(x, y)
        replay = input("\033[1;35mGame over. Press Enter to start a new game, or type 'exit' to quit: \033[0m").strip()
        if replay.lower() in ("exit", "quit"):
            break