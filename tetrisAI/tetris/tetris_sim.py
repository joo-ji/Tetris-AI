import copy
import math
import random
import numpy as np

import config as cfg
from playfield import Playfield
from tetromino import Tetromino

TETROMINO_LIST = [
    Tetromino(shape='I'),
    Tetromino(shape='J'),
    Tetromino(shape='L'),
    Tetromino(shape='O'),
    Tetromino(shape='S'),
    Tetromino(shape='T'),
    Tetromino(shape='Z')
]

def generate_tetromino_sequence():
    tetromino_list_copy = copy.deepcopy(TETROMINO_LIST)
    random.shuffle(tetromino_list_copy)
    return tetromino_list_copy

def run_simulation(playgrid, weights):
    tetro_list = generate_tetromino_sequence()
    score = 0;
    piece_count = 0
    while(piece_count < cfg.NUM_PIECES_SIM):
        if not tetro_list:
            tetro_list = generate_tetromino_sequence()
        try:
            run(tetro_list.pop(), playgrid, weights)
            if(playgrid.consecutive_lines > 1):
                score += math.pow(2, playgrid.consecutive_lines - 2)

            piece_count += 1
        except (IndexError, ValueError):
            score += piece_count * 0.05
            return score, piece_count
            score += piece_count * 0.05
    return score, piece_count

def run(input_tetro, playgrid, weights):
    best_position = input_tetro.position_state
    best_rotation = input_tetro.rotation_state
    best_score = 0
    best_features = []
    for i in range(0, input_tetro.rotations):

        for j in range(0, input_tetro.positions):
            test_grid = copy.deepcopy(playgrid)
            test_grid.fast_drop(input_tetro)
            features = get_features(playgrid, test_grid)
            fitness_score = evaluate_fitness(features, weights)
            if(fitness_score > best_score):
                best_features = features
                best_score = fitness_score
                best_position = input_tetro.position_state
                best_rotation = input_tetro.rotation_state
            input_tetro.shift_right()

        input_tetro.rotate_clockwise()
    drop_tetromino(input_tetro, playgrid, best_position, best_rotation)
    return best_position, best_rotation, best_score, best_features

def drop_tetromino(input_tetro, playgrid, position, rotation):
    input_tetro.rotate_clockwise_to(rotation)
    input_tetro.shift_right_to(position)
    playgrid.fast_drop(input_tetro)

def evaluate_fitness(features, weights):
    return np.dot(features, weights)

def get_features(playgrid, test_grid):
    lines_cleared = get_lines_cleared(test_grid)
    consec_lines = get_consecutive_lines_cleared(test_grid)
    abs_height = get_absolute_height(test_grid)
    rel_height = get_relative_height(test_grid)
    cumulative_height = get_cumulative_height(test_grid)
    new_holes = get_holes(playgrid, test_grid)
    well_depth = get_well_depth(test_grid)
    roughness = get_roughness(test_grid)
    return np.array( [lines_cleared, consec_lines, abs_height, rel_height, cumulative_height, new_holes, well_depth, roughness] );

def get_lines_cleared(test_grid):
    return test_grid.lines_cleared

def get_consecutive_lines_cleared(test_grid):
    return test_grid.consecutive_lines

def get_absolute_height(test_grid):
    return np.amax(test_grid.grid_height)

# function to evaluate the difference in the max and min height
def get_relative_height(test_grid):
    return np.amax(test_grid.grid_height) - np.amin(test_grid.grid_height)

def get_cumulative_height(test_grid):
    return np.sum(test_grid.grid_height)

# function to evaluate if a 'hole' is created
def get_holes(playgrid, test_grid):
    return (test_grid.grid_height - playgrid.grid_height).sum() - 4 + cfg.WIDTH * test_grid.lines_cleared

def get_hole_depth(playgrid):
    print()

def get_roughness(test_grid):
    return np.absolute((test_grid.grid_height[0: cfg.WIDTH - 1] - test_grid.grid_height[1: cfg.WIDTH])).sum()

def get_well_depth(test_grid):
    well_depth = 0
    for i in range(1, cfg.WIDTH - 1):
        left = test_grid.grid_height[i - 1] - test_grid.grid_height[i]
        right = test_grid.grid_height[i + 1] - test_grid.grid_height[i]
        if(left > 2 and right > 2):
            well_depth += min(left, right)

    l_edge = test_grid.grid_height[1] - test_grid.grid_height[0]
    if(l_edge > 2):
        well_depth += l_edge

    r_edge = test_grid.grid_height[cfg.WIDTH- 2] - test_grid.grid_height[cfg.WIDTH - 1]
    if(r_edge > 2):
        well_depth += r_edge

    return well_depth

def print_self(playgrid):
    playgrid.print_self()
