import numpy as np
import config as cfg

class Tetromino:
    TETROMINOS = {
            'I':(
                    2,
                    3,
                    np.array(
                            [[1, 1, 1, 1]],
                             )
                ),
            'J':(
                    4,
                    3,
                    np.array(
                            [[1, 0, 0],
                             [1, 1, 1]],
                            )
                ),
            'L':(
                    4,
                    3,
                    np.array(
                            [[0, 0, 1],
                             [1, 1, 1]],
                             )
                ),
            'O':(
                    1,
                    4,
                    np.array(
                            [[1, 1],
                             [1, 1]],
                            )
                ),
            'S':(
                    4,
                    3,
                    np.array(
                            [[0, 1, 1],
                            [1, 1, 0]],
                            )
                ),
            'T':(
                    4,
                    3,
                    np.array(
                            [[0, 1, 0],
                             [1, 1, 1]],
                            )
                ),
            'Z':(
                    4,
                    3,
                    np.array(
                            [[1, 1, 0],
                             [0, 1, 1]],
                            )
                )
    }
    COLOR_SHAPE_MAP = {
            (50, 190, 250): 'I',
            (68, 100, 233): 'J',
            (255, 126, 37): 'L',
            (255, 194, 37): 'O',
            (124, 212, 36): 'S',
            (210, 76, 173): 'T',
            (250, 50, 90): 'Z'
    }
    SPAWN_POSITION = 3

    def __init__(self, color=None, shape=None):
        self.rotation_state = 0
        if(color != None):
            self.color = color
            shape = self.COLOR_SHAPE_MAP[color]
        if(shape != None):
            self.shape = shape
            self.rotations, self.position_state, self.matrix = self.TETROMINOS[shape]
            self.update_matrix()

    def rotate_clockwise(self):
        if(self.shape != 'O'):
            self.matrix = np.rot90(self.matrix, 1, (1, 0))
            self.rotation_state = (self.rotation_state + 1) % self.rotations
            self.update_matrix()

    def rotate_clockwise_to(self, end_state):
        while(self.rotation_state != end_state):
            self.rotate_clockwise()

    def shift_right(self):
        self.position_state = (self.position_state + 1) % self.positions

    def shift_right_to(self, end_state):
        while(self.position_state != end_state):
            self.shift_right()

    def update_matrix(self):
        self.height = len(self.matrix)
        self.width = len(self.matrix[0, :])
        self.positions = cfg.WIDTH - self.width + 1
        if(self.rotation_state == 1):
            if(self.shape == 'I'):
                self.position_state += 2
            else:
                self.position_state += 1
        elif(self.rotation_state == 2):
            if(self.shape == 'I'):
                self.position_state -= 2
            else:
                self.position_state -= 1

    def print_tetromino(self):
        print("shape: ", self.shape)
        print("rotation state: ", self.rotation_state)
        print("position state: ", self.position_state)
        print("matrix: \n", self.matrix)
