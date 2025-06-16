import random

CELL_SIZE = 40
GRID_SIZE = 10
MINES_COUNT = 10

class Game:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.grid = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.flags = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        self.game_over = False
        self.won = False
        self.place_mines()
        self.calculate_numbers()

    def place_mines(self):
        mines_placed = 0
        while mines_placed < MINES_COUNT:
            x = random.randint(0, GRID_SIZE - 1)
            y = random.randint(0, GRID_SIZE - 1)
            if self.grid[y][x] != -1:
                self.grid[y][x] = -1
                mines_placed += 1

    def calculate_numbers(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] != -1:
                    count = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                                if self.grid[ny][nx] == -1:
                                    count += 1
                    self.grid[y][x] = count

    def reveal_cell(self, x, y):
        if self.revealed[y][x] or self.flags[y][x] or self.game_over:
            return
        self._reveal_recursive(x, y)
        self._check_win_condition()

    def _reveal_recursive(self, x, y):
        if self.revealed[y][x] or self.flags[y][x]:
            return
        self.revealed[y][x] = True
        if self.grid[y][x] == -1:
            self.game_over = True
            return
        if self.grid[y][x] == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE:
                        self._reveal_recursive(nx, ny)

    def _check_win_condition(self):
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                if self.grid[y][x] != -1 and not self.revealed[y][x]:
                    return
        self.won = True

    def toggle_flag(self, x, y):
        if not self.revealed[y][x]:
            self.flags[y][x] = not self.flags[y][x]

    def get_state(self):
        # Eğer oyun bittiyse, tüm mayınlar görünür olsun
        display_grid = [
            [self.grid[y][x] if self.revealed[y][x] or self.game_over else None for x in range(GRID_SIZE)]
            for y in range(GRID_SIZE)
        ]
        return {
            "grid": display_grid,
            "revealed": self.revealed,
            "flags": self.flags,
            "game_over": self.game_over,
            "won": self.won
        }
