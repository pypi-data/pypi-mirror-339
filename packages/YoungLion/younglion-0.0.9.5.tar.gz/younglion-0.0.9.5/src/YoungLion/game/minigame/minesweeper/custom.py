import re
import random
from typing import List, Tuple
class MinesweeperGameStatus:
    """
    Defines game status codes.
      - starting: Game hasn't begun yet.
      - continue: Game is in progress.
      - lose: Game over (a mine was hit).
      - win: Game won (all non-mine cells revealed).
      - none: No move was made because the cell was already clicked.
    """
    starting = 0
    continue_ = 1
    lose = 2
    win = 3
    none = 4
class MinesweeperHelp:
    """
    Provides help and documentation for the Minesweeper game.
    
    Help can cover various topics (general, developer, usage, functions, etc.)
    using ANSI escape codes to colorize the terminal output. Additionally,
    a Markdown formatted version of the help text can be obtained.
    """
    def __init__(self, topic: str = "general"):
        """
        Initializes the help instance with the specified topic.
        
        Args:
            topic (str): The topic for which help is requested.
                         Options include "general", "developer", "usage", and "functions".
                         Defaults to "general". If an unknown topic is provided, "general" is used.
        """
        self.topic = topic.lower()
        self.help_texts = {
            "general": (
                "\033[1;36mMinesweeper Game Help (General)\033[0m\n"
                "This Minesweeper game is designed as a library that can be easily integrated into your application.\n"
                "It provides an interactive terminal version with colorized output and intuitive controls.\n"
                "At any time during the game, type 'help' to see these instructions again."
            ),
            "developer": (
                "\033[1;35mMinesweeper Developer Help\033[0m\n"
                "Classes:\n"
                "  - CustomMinesweeper: Contains the game logic, board setup, move processing, and operator overloads.\n"
                "  - MinesweeperMap: Handles the board representation with a 2D grid of cells.\n"
                "\n"
                "Usage:\n"
                "  - Create a new game by initializing CustomMinesweeper with board size and mine count.\n"
                "  - Use the make_move(x, y) method to process user moves.\n"
                "  - The __add__ operator is overloaded for combining boards.\n"
                "Refer to the source code for more details and customization options."
            ),
            "usage": (
                "\033[1;32mMinesweeper Usage Help\033[0m\n"
                "To play the game in the terminal:\n"
                "  - Input the board dimensions and mine count when prompted.\n"
                "  - In each move, type two integers separated by a space (e.g. '3 4') corresponding to the row and column to reveal.\n"
                "  - Use commands like 'help' for instructions and 'exit' or 'quit' to leave the game.\n"
                "The game interface displays coordinate labels and highlights your last move."
            ),
            "functions": (
                "\033[1;33mMinesweeper Functions Help\033[0m\n"
                "Key functions and methods:\n"
                "  - make_move(x, y): Processes a move and updates the game board.\n"
                "  - __add__(other): Combines two Minesweeper boards element-wise.\n"
                "  - _flood_fill(x, y): Reveals connected empty cells recursively.\n"
                "\n"
                "Use these functions as part of the API to integrate Minesweeper in your project."
            ),
        }
        if self.topic not in self.help_texts:
            self.topic = "general"
    def get_help(self) -> str:
        """
        Returns the help text for the selected topic in ANSI colored format.
        """
        return self.help_texts.get(self.topic, self.help_texts["general"])
    def __str__(self) -> str:
        """
        Returns the ANSI colored help text.
        """
        return self.get_help()
    def to_markdown(self) -> str:
        """
        Returns the help text formatted in Markdown.
        
        ANSI escape codes are stripped out.
        """
        ansi_escape = re.compile(r'\033\[[0-9;]*m')
        raw_text = self.get_help()
        md_text = ansi_escape.sub('', raw_text)
        return f"```\n{md_text}\n```"
    @staticmethod
    def list_topics() -> str:
        """
        Returns a string listing the available help topics.
        """
        topics = list(["general", "developer", "usage", "functions"])
        return "Available topics: " + ", ".join(topics)
class MinesweeperMap:
    """
    Represents the game board (map) for Minesweeper.
    
    The board is internally stored as a 2D list of tuples:
      - First element (int): The cell's value (-1 for mine, 0 for empty, positive for adjacent mine count).
      - Second element (bool): Visibility flag (True if the cell is revealed).
    
    This class provides a custom __str__ method that returns a human-readable string representation.
    Hidden cells are displayed with a hidden symbol.
    """
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.grid: List[List[Tuple[int, bool]]] = [[(0, False) for _ in range(cols)] for _ in range(rows)]
    def __getitem__(self, index: int) -> List[Tuple[int, bool]]:
        return self.grid[index]
    def __setitem__(self, index: int, value: List[Tuple[int, bool]]):
        self.grid[index] = value
    def __str__(self) -> str:
        """
        Returns a string representation of the board.
        
        For each cell:
          - If the cell is not visible, a hidden cell symbol ("□") is shown.
          - If the cell is visible and is a mine, a mine symbol ("*") is shown.
          - If the cell is visible and has a 0 value, an empty space (" ") is shown.
          - Otherwise, the cell's numeric value is displayed.
        """
        rows_str = []
        for row in self.grid:
            row_repr = []
            for value, visible in row:
                if not visible:
                    row_repr.append("□")
                else:
                    if value == -1:
                        row_repr.append("*")
                    elif value == 0:
                        row_repr.append(" ")
                    else:
                        row_repr.append(str(value))
            rows_str.append(" ".join(row_repr))
        return "\n".join(rows_str)
class CustomMinesweeper:
    """
    A custom Minesweeper game implementation designed as a library.
    
    Attributes:
        size (Tuple[int, int]): The dimensions of the game board as (rows, cols).
        mines_count (int): The number of mines to be placed on the board.
        max_neighbors (int): Maximum allowed mines in the neighbors for placing a new mine.
        game_map (MinesweeperMap): The game board wrapped in a MinesweeperMap instance.
    """
    
    def __init__(self, size: Tuple[int, int], mines_count: int, max_neighbors: int = 5):
        """
        Initializes the game board and places mines.
        
        Args:
            size (Tuple[int, int]): (rows, cols) specifying board dimensions.
            mines_count (int): The number of mines to place.
            max_neighbors (int, optional): Maximum number of mines allowed in neighbors for a new mine.
                                           Defaults to 5.
        """
        self.size = size
        self.mines_count = mines_count
        self.max_neighbors = max_neighbors
        rows, cols = size
        self.game_map = MinesweeperMap(rows, cols)
        self._place_mines()
        self.status = MinesweeperGameStatus.starting
    def __str__(self) -> str:
        """
        Returns a string representation of the game board.
        
        Delegates to MinesweeperMap.__str__ to display hidden cells as a hidden symbol.
        """
        return str(self.game_map)
    def _random_coordinate(self) -> Tuple[int, int]:
        """
        Generates a random coordinate within the bounds of the board.
        
        Returns:
            Tuple[int, int]: A random (row, col) coordinate.
        """
        rows, cols = self.size
        return random.randint(0, rows - 1), random.randint(0, cols - 1)
    def _get_neighbors(self, x: int, y: int) -> List[Tuple[int, int]]:
        """
        Retrieves valid neighboring cell coordinates (8 directions) for a given cell.
        
        Args:
            x (int): Row index of the cell.
            y (int): Column index of the cell.
        
        Returns:
            List[Tuple[int, int]]: List of (row, col) tuples for neighboring cells.
        """
        neighbors = []
        rows, cols = self.size
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                neighbors.append((nx, ny))
        return neighbors
    def _place_mines(self) -> None:
        """
        Places mines on the board ensuring that no cell's neighbors exceed
        the specified max_neighbors mines. For each mine placed, increments the value of
        its neighboring cells (if they are not mines).
        """
        rows, cols = self.size
        placed_mines = 0
        while placed_mines < self.mines_count:
            x, y = self._random_coordinate()
            if self.game_map[x][y][0] == -1:
                continue
            neighbors = self._get_neighbors(x, y)
            close_mines = sum(1 for nx, ny in neighbors if self.game_map[nx][ny][0] == -1)
            if close_mines >= self.max_neighbors:
                continue
            self.game_map[x][y] = (-1, False)
            placed_mines += 1
            for nx, ny in neighbors:
                if self.game_map[nx][ny][0] != -1:
                    current_value, visible = self.game_map[nx][ny]
                    self.game_map[nx][ny] = (current_value + 1, visible)
    def __add__(self, other: 'CustomMinesweeper') -> 'CustomMinesweeper':
        """
        Overloads the addition operator to combine two game boards element-wise.
        
        For each corresponding cell:
          - If either cell is a mine (value -1), the resulting cell is a mine.
          - Otherwise, the cell's value is the sum of the two cells' values.
          - The cell is marked visible if at least one of the cells is visible.
        
        Args:
            other (CustomMinesweeper): Another game instance to combine with.
        
        Returns:
            CustomMinesweeper: A new game instance with the combined board.
            
        Raises:
            ValueError: If the boards' dimensions do not match.
        """
        if self.size != other.size:
            raise ValueError("Boards must be of the same dimensions to add them.")
        rows, cols = self.size
        new_map = MinesweeperMap(rows, cols)
        for i in range(rows):
            for j in range(cols):
                val1, vis1 = self.game_map[i][j]
                val2, vis2 = other.game_map[i][j]
                if val1 == -1 or val2 == -1:
                    new_map[i][j] = (-1, vis1 or vis2)
                else:
                    new_map[i][j] = (val1 + val2, vis1 or vis2)
        new_game = CustomMinesweeper(self.size, 0)
        new_game.game_map = new_map
        return new_game
    def make_move(self, x: int, y: int) -> Tuple[MinesweeperMap, int]:
        """
        Processes a player's move (click) on the board at coordinates (x, y).
        
        Reveals the cell at (x, y) and applies a flood-fill if the cell's value is 0.
        Returns the updated MinesweeperMap and a status code:
          - 0: Game continues.
          - 1: Game lost (mine clicked).
          - 2: Game won (all non-mine cells revealed).
        
        Args:
            x (int): Row index to click.
            y (int): Column index to click.
        
        Returns:
            Tuple[MinesweeperMap, int]: The updated game map and status code.
        
        Raises:
            IndexError: If the specified coordinates are out of bounds.
        """
        rows, cols = self.size
        if not (0 <= x < rows and 0 <= y < cols):
            raise IndexError("Cell coordinates out of bounds.")
        cell_value, cell_visible = self.game_map[x][y]
        if cell_visible:
            self.status = MinesweeperGameStatus.none  
            return (self.game_map, self.status)
        self.game_map[x][y] = (cell_value, True)
        if cell_value == -1:
            for i in range(rows):
                for j in range(cols):
                    if self.game_map[i][j][0] == -1:
                        self.game_map[i][j] = (-1, True)  
            self.status = MinesweeperGameStatus.lose 
            return (self.game_map, self.status)
        if cell_value == 0:
            self._flood_fill(x, y)
        for i in range(rows):
            for j in range(cols):
                value, visible = self.game_map[i][j]
                if value != -1 and not visible:
                    self.status = MinesweeperGameStatus.continue_  
                    return (self.game_map, self.status)
        self.status = MinesweeperGameStatus.win  
        return (self.game_map, self.status)
    def _flood_fill(self, x: int, y: int) -> None:
        """
        Reveals all connected empty cells (with a value of 0) using flood-fill.
        
        This method is called when an empty cell is revealed and recursively
        reveals adjacent cells.
        
        Args:
            x (int): Row index of the starting cell.
            y (int): Column index of the starting cell.
        """
        rows, cols = self.size
        stack = [(x, y)]
        visited = set((x, y))
        while stack:
            cx, cy = stack.pop()
            for nx, ny in self._get_neighbors(cx, cy):
                if (nx, ny) in visited:
                    continue
                cell_value, cell_visible = self.game_map[nx][ny]
                if not cell_visible:
                    self.game_map[nx][ny] = (cell_value, True)
                if cell_value == 0:
                    stack.append((nx, ny))
                    visited.add((nx, ny))
