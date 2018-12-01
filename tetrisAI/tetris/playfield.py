import numpy as np
import timeit

from tetromino import Tetromino

class Playfield:
    HEIGHT = 21
    WIDTH = 10
    
    def __init__(self):
        self.grid = np.zeros((self.HEIGHT, self.WIDTH))
        self.combo = False
        
 #       self.grid[self.HEIGHT - 10, :] = 1
  #      self.grid[self.HEIGHT - 15, :] = 1
        self.grid[self.HEIGHT - 7, :] = 1
        #print("initial playfield:\n", self.grid)
    
    def print_self(self):
        print(self.grid)
    
    def spawn_tetromino(self, shape):
        return Tetromino(shape, self.SPAWN_POSITION)
    
    def get_drop_level(self, tetroblock):
        drop_area = self.grid[:, tetroblock.position_state:(tetroblock.position_state + tetroblock.width)]
        #print("drop area: \n", drop_area)
        for i in range(0, self.HEIGHT - tetroblock.height + 1):
            temp_area = drop_area[i:(i + tetroblock.height), :]
            #print("temp area\n", temp_area)
            tetromino_drop = temp_area + tetroblock.matrix
            #print("tetromino\n", tetromino_drop)
            
            if 2 in tetromino_drop:
                return i - 1
        
        return self.HEIGHT - tetroblock.height            
    
    def fast_drop(self, tetroblock):
        drop_level = self.get_drop_level(tetroblock)
        #print("current space\n", self.grid[drop_level:(drop_level + tetroblock.height), :][:, tetroblock.position_state:(tetroblock.position_state + tetroblock.width)])
        self.grid[drop_level:(drop_level + tetroblock.height), :][:, tetroblock.position_state:(tetroblock.position_state + tetroblock.width)] += tetroblock.matrix
        #print(self.grid)
        self.clear_line()
        self.update_block_height()
    
    def clear_line(self):
      #  for i in range(level, level + tetroblock.height):
       #     if(np.all(self.grid[i, :] == 1)):
        #        self.grid = numpy.delete(self.grid, i, 0)
        self.grid = self.grid[~np.all(self.grid == 1, axis = 1)]
        
        if(self.HEIGHT - len(self.grid) > 0):
            new_grid = np.zeros((self.HEIGHT - len(self.grid), self.WIDTH))
            self.grid = np.concatenate((new_grid, self.grid), axis = 0)
            self.combo = True
        else:
            self.combo = False
    
    def update_block_height(self):
        #print("\nplayfield\n", self.grid)
        self.placed_height = self.grid.argmax(axis = 0)
        self.placed_height[self.placed_height == 0] = self.HEIGHT        
        self.relative_height = self.placed_height - np.amax(self.placed_height)
        self.empty_height = self.HEIGHT - 1 - np.flip(self.grid, 0).argmin(axis = 0)
        self.height_diff = np.amax(self.relative_height[0: self.WIDTH - 1]) - np.amin(self.relative_height[0: self.WIDTH - 1])
        
        #print("\nplaced height\n", self.placed_height)
        #print("relative height\n", self.relative_height)
        #print("empty height\n", self.empty_height)
        #print("height_diff\n", self.height_diff)
    
    def should_clear(self, clear_level):
        return np.all(self.placed_height < clear_level)
    
    def test_time(self):
        print(timeit.timeit(self.update_block_height, number=1000))
        print("efficiency test")
    