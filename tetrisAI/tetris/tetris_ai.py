import copy
import timeit
import numpy as np

from tetromino import Tetromino
from playfield import Playfield

class Tetris_AI:
    
    CLEAR_LEVEL = 13
    hold_piece = 0
    
    def __init__(self):
        self.playgrid = Playfield()
    
    def hold_tetromino(self, tetro_color):
        if(tetro_color == (43, 43, 43)):
            return False
        elif(self.hold_piece == 0):
            self.hold_piece = Tetromino((tetro_color))
            return True
        elif(tetro_color != (44, 209, 255) or self.hold_piece.color == (44, 209, 255)):
            return False
        else:
            self.hold_piece = Tetromino((44, 209, 255))
            return True
    
    def clear_mode(self, tetro_color):
        if(np.all(self.playgrid.placed_height[0: self.playgrid.WIDTH - 1] < self.CLEAR_LEVEL) and (tetro_color == self.hold_piece.color == (44, 209, 255))):
            return True
        else:
            return False
    
    def run_ai(self, tetro_block, clearing):    
        if(clearing):
            best_position = self.playgrid.WIDTH - 1
            best_rotation = 1
            fitness_score = 100
            fit_array = [1, 60, 20, 20]
            self.drop_tetromino(tetro_block, best_position, best_rotation)
            return best_position, best_rotation, fitness_score, fit_array
        else:
            best_position = tetro_block.position_state
            best_rotation = tetro_block.rotation_state
            fitness_score = 0
            for i in range(0, tetro_block.rotations):
                
                for i in range(0, tetro_block.positions):
                    test_grid = copy.deepcopy(self.playgrid)
                    test_grid.fast_drop(tetro_block)
                    
                    fitness = self.evaluate_fitness(test_grid)
                    score =  fitness[0] * (fitness[1] + fitness[2] + fitness[3])
                    if(score > fitness_score):
                        fitness_score = score
                        fit_array = fitness
                        best_position = tetro_block.position_state
                        best_rotation = tetro_block.rotation_state
                    
                    tetro_block.shift_right()
                
                tetro_block.rotate_matrix()
            
            self.drop_tetromino(tetro_block, best_position, best_rotation)
            return best_position, best_rotation, fitness_score, fit_array
    
    def drop_tetromino(self, tetro_block, position, rotation):
        tetro_block.rotate_matrix_to(rotation)
        tetro_block.shift_right_to(position)
        self.playgrid.fast_drop(tetro_block)
    
    def evaluate_fitness(self, test_grid):
        #print("evaluate holes:", self.evaluate_holes(test_grid))
        #print("evaluate height:", self.evaluate_height(test_grid))
        #print("evaluate height difference:", self.evaluate_height_diff(test_grid))
        
        clear_col = self.evaluate_clear_columns(test_grid)
        #print("clear_factor score: ", clear_factor)
        holes = 60 * self.evaluate_holes(test_grid)
        #print("hole score: ", holes)
        h_level = 20 * self.evaluate_height(test_grid)
        #print("height level: ", h_level)
        h_diff = 20 * self.evaluate_height_diff(test_grid)
        #print("height diff: ", h_diff)
        
        #total_score = clear_factor * (holes + h_level + h_diff)
        #print("total score:", total_score)
        #return total_score
        return np.array( [clear_col, holes, h_level, h_diff] );
    
    def evaluate_complete_columns(self, test_grid):
        return 0
            
    # function to evaluate if the AI should clear or not
    def evaluate_clear_columns(self, test_grid):
        if(np.all(self.playgrid.placed_height[0: self.playgrid.WIDTH - 1] < self.CLEAR_LEVEL)):
            return 0.8
        
        if(test_grid.placed_height[test_grid.WIDTH - 1: test_grid.WIDTH] < self.playgrid.placed_height[self.playgrid.WIDTH - 1: self.playgrid.WIDTH]):
            return 0.5
        
        if(test_grid.cleared_lines != 0):
            return 0.6
        
        return 1
    
    # function to evaluate if a 'hole' is create
    def evaluate_holes(self, test_grid):
        spaces_filled = np.sum(self.playgrid.placed_height) - np.sum(test_grid.placed_height) - 10 * test_grid.cleared_lines
        return 4 / spaces_filled
    
    # another function to evaluate holes
    def evaluate_holes_2(self, test_grid):
        if(np.any(np.subtract(test_grid.placed_height, test_grid.empty_height) != 1)):
            return 0.6
        return 1
    
    def evaluate_height(self, test_grid):
        avg_comparison = (test_grid.placed_height < np.mean(test_grid.placed_height)).sum()
        return avg_comparison / 10;
    
    # function to evaluate the difference in the max and min height
    def evaluate_height_diff(self, test_grid):
        height_d = np.amax(test_grid.placed_height[0: test_grid.WIDTH - 1]) - np.amin(test_grid.placed_height[0: test_grid.WIDTH - 1])
        return (test_grid.HEIGHT - height_d * 1.5) / test_grid.HEIGHT
    
    def print_self(self):
        self.playgrid.print_self()
    
    def time_test(self):
        print(timeit.timeit(self.run_ai(Tetromino((255, 156, 35))), number=10))
        print("efficiency test")
    