import numpy as np

import config as cfg

class Playfield:

    def __init__(self):
        self.grid = np.zeros((cfg.HEIGHT, cfg.WIDTH))
        self.lines_cleared = 0
        self.consecutive_lines = 0
        self.update_grid_parameters()
        # self.pieces = 0

    def get_drop_level(self, tetroblock):
        drop_area = self.grid[:, tetroblock.position_state:(tetroblock.position_state + tetroblock.width)]

        for i in range(0, cfg.HEIGHT - tetroblock.height + 1):
            temp_area = drop_area[i:(i + tetroblock.height), :]
            tetromino_drop = temp_area + tetroblock.matrix
            if 2 in tetromino_drop:
                return i - 1

        return cfg.HEIGHT - tetroblock.height

    def fast_drop(self, tetroblock):
        drop_level = self.get_drop_level(tetroblock)
        self.grid[drop_level:(drop_level + tetroblock.height), :][:, tetroblock.position_state:(tetroblock.position_state + tetroblock.width)] += tetroblock.matrix
        self.update_board()
        self.update_grid_parameters()

    def update_board(self):
        # self.pieces += 1
        self.grid = self.grid[~np.all(self.grid == 1, axis = 1)]

        if(cfg.HEIGHT - len(self.grid) > 0):
            new_grid = np.zeros((cfg.HEIGHT - len(self.grid), cfg.WIDTH))
            self.grid = np.concatenate((new_grid, self.grid), axis = 0)
            self.lines_cleared = len(new_grid)
            self.consecutive_lines += len(new_grid)
        else:
            self.lines_cleared = 0
            self.consecutive_lines = 0

    def update_grid_parameters(self):
        self.grid_height = self.grid.argmax(axis = 0)
        self.grid_height[self.grid_height != 0] = cfg.HEIGHT - self.grid_height[self.grid_height != 0]

    def print_self(self):
        print(self.grid)
