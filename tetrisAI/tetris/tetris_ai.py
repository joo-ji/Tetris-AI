import copy
import numpy as np
import timeit

from tetromino import Tetromino
from playfield import Playfield

class Tetris_AI:
    def __init__(self):
        self.playgrid = Playfield()
        #self.playgrid.grid[self.playgrid.HEIGHT - 1, :] = 1
        self.playgrid.combo = True
        print("\nai playgrid\n", self.playgrid.grid)
        test = Tetromino('L')
        self.playgrid.fast_drop(test)
    #def calculate_fitness(self):
        #
    
    def run_ai(self):
        test_block = Tetromino('L')
        
        best_position = test_block.position_state
        best_rotation = test_block.rotation_state
        fit_score = 0
        
        for i in range(0, test_block.rotations):
            
            for i in range(0, test_block.positions):
                test_grid = copy.deepcopy(self.playgrid)
                test_grid.fast_drop(test_block)
                
                if(self.evaluate_fitness(test_grid) > fit_score):
                    fit_score = self.evaluate_fitness(test_grid)
                    best_position = test_block.position_state
                    best_rotation = test_block.rotation_state
                    
                test_block.shift_right()
            
            test_block.rotate_matrix()
        
        #print(test_grid)
        return best_position, best_rotation
    
    def evaluate_fitness(self, test_grid):
        print(self.evaluate_holes(test_grid))
        return 0
        
        
    def evaluate_clear_columns(self, test_grid):
        if(self.playgrid.should_clear()):
            if(test_grid.combo):
                return 1
            return 0.7
        
        if(test_grid.combo):
            return 0.5
        
        return 1
            #if 1 in self.playgrid.grid[:, self.playgrid.WIDTH - 2]:
            #    if 1 in self.playgrid.grid[:, self.playgrid.WIDTH - 1]:
            #        return 1
            #    else:
            #        
            #        return 0.2
            
            #return 0.6        
    
    def evaluate_holes(self, test_grid):
        test_relative_height = test_grid.placed_height - np.amax(test_grid.placed_height)
        
        if(np.sum(self.playgrid.relative_height) - np.sum(test_relative_height) == 4):
            return 1
        return 0.6
    
    # another function to evaluate holes
    def evaluate_holes_2(self, test_grid):
        if(np.any(np.subtract(test_grid.placed_height, test_grid.empty_height) != 1)):
            return 0.6
        
        return 1
    
    def evaluate_height(self, test_grid):
        
    def time_test(self):
        print(timeit.timeit(self.run_ai, number=10))
        print("efficiency test")