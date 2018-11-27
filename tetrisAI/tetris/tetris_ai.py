import copy
import timeit
import math
import numpy as np

from tetromino import Tetromino
from playfield import Playfield

class Tetris_AI:
    
    CLEAR_LEVEL = 13
    
    def __init__(self):
        self.playgrid = Playfield()
        #self.playgrid.grid[self.playgrid.HEIGHT - 1, :] = 1
        #self.playgrid.combo = True
        #print("\nai playgrid\n", self.playgrid.grid)
        #test = Tetromino((255, 156, 35))
        #self.playgrid.fast_drop(test)
    #def calculate_fitness(self):
        #
    def print_self(self):
        self.playgrid.print_self()
    
    def run_ai(self, tetro_block):        
        best_position = tetro_block.position_state
        best_rotation = tetro_block.rotation_state
        fit_score = 0
        
        for i in range(0, tetro_block.rotations):
            #print("rotation state: ", tetro_block.rotation_state)
            #print("before rotation:\n", tetro_block.matrix)
            
            for i in range(0, tetro_block.positions):
                test_grid = copy.deepcopy(self.playgrid)
                test_grid.fast_drop(tetro_block)
                
                if(self.evaluate_fitness(test_grid) > fit_score):
                    fit_score = self.evaluate_fitness(test_grid)
                    best_position = tetro_block.position_state
                    best_rotation = tetro_block.rotation_state
                
                #print("position state before shift: ", tetro_block.position_state)
                tetro_block.shift_right()
            
            tetro_block.rotate_matrix()
        
        #print("fitness score: ", fit_score)
        self.drop_tetromino(tetro_block, best_position, best_rotation)
        return best_position, best_rotation
    
    def drop_tetromino(self, tetro_block, position, rotation):
        tetro_block.rotate_matrix_to(rotation)
        tetro_block.shift_right_to(position)
        self.playgrid.fast_drop(tetro_block)
        
    def evaluate_fitness(self, test_grid):
        #print("evaluate holes:", self.evaluate_holes(test_grid))
        #print("evaluate height:", self.evaluate_height(test_grid))
        #print("evaluate height difference:", self.evaluate_height_diff(test_grid))
        
        factor = self.evaluate_clear_columns(test_grid)
        holes = 40 * self.evaluate_holes(test_grid)
        h_level = 40 * self.evaluate_height(test_grid)
        h_diff = 20 * self.evaluate_height_diff(test_grid)
        
        total_score = factor * (holes + h_level + h_diff)
        #print("total score:", total_score)
        return total_score
        
    # function to evaluate if the AI should clear or not
    def evaluate_clear_columns(self, test_grid):
        if(self.playgrid.should_clear(self.CLEAR_LEVEL)):
            if(test_grid.combo):
                return 1
            return 0.75
        
        if(test_grid.relative_height[test_grid.WIDTH - 1: test_grid.WIDTH] != 0):
            return 0.5
        
        if(test_grid.combo):
            return 0.6
        
        return 1
            #if 1 in self.playgrid.grid[:, self.playgrid.WIDTH - 2]:
            #    if 1 in self.playgrid.grid[:, self.playgrid.WIDTH - 1]:
            #        return 1
            #    else:
            #        
            #        return 0.2
            
            #return 0.6        
    
    # function to evaluate if a 'hole' is create
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
        if((test_grid.placed_height < math.floor((np.mean(test_grid.placed_height) + 2))).sum() >= (self.playgrid.placed_height < math.floor((np.mean(self.playgrid.placed_height) + 2))).sum()):
            return 1
        return 0.6
            
    # function to evaluate the difference in the max and min height
    def evaluate_height_diff(self, test_grid):
        height_d = np.amax(test_grid.relative_height[0: test_grid.WIDTH - 1]) - np.amin(test_grid.relative_height[0: test_grid.WIDTH - 1])
        #print(test_grid.relative_height[0: test_grid.WIDTH - 1])
        #print("height diff:", height_d)
        if(height_d < math.ceil(test_grid.HEIGHT / 4) or height_d < self.playgrid.height_diff):
            return 1
        return 0.6
    
    def time_test(self):
        print(timeit.timeit(self.run_ai(Tetromino((255, 156, 35))), number=10))
        print("efficiency test")