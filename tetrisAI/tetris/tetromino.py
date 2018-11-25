import numpy as np

class Tetromino:
    TETROMINO_TYPE = {
            'I':(
                    np.array(
                            [[1, 1, 1, 1]],
                             ),
                    (37, 123, 143),
                    2
                ),
            'J':(
                    np.array(
                            [[1, 0, 0],
                             [1, 1, 1]],
                            ),
                    (36, 71, 153),
                    4
                ),
            'L':(
                    np.array(
                            [[0, 0, 1],
                             [1, 1, 1]],
                             ),
                    (188, 86, 35),
                    4
                ),
            'O':(
                    np.array(
                            [[1, 1],
                             [1, 1]],
                            ),
                    (255, 210, 0),
                    1
                ),
            'S':(
                    np.array(
                            [[0, 1, 1],
                            [1, 1, 0]],
                            ),
                    (37, 127, 36),
                    4
                ),
            'T':(
                    np.array(
                            [[0, 1, 0],
                             [1, 1, 1]],
                            ),
                    (137, 35, 137),
                    4
                ),
            'Z':(
                    np.array(
                            [[1, 1, 0],
                             [0, 1, 1]],
                            ),
                    (193, 47, 76),
                    4
                )
    }
    
    SPAWN_POSITION = 3
    BOARD_SIZE = 10
    
    def __init__(self, shape):
        self.shape = shape
        self.rotation_state = 0
        self.create_Tetromino()
        
        self.position_state = self.SPAWN_POSITION
        if(shape == 'O'):
            self.position_state += 1
        
        
    def create_Tetromino(self):
        self.matrix, self.color, self.rotations = self.TETROMINO_TYPE[self.shape]
        self.height = len(self.matrix)
        self.width = len(self.matrix[0,:])
        self.positions = self.BOARD_SIZE - self.width + 1
        
    def rotate_matrix(self):
        if(self.shape != 'O'):
            self.matrix = np.rot90(self.matrix, 1, (1, 0))
            self.rotation_state = (self.rotation_state + 1) % self.rotations
            self.height = len(self.matrix)
            self.width = len(self.matrix[0,:])
            self.positions = self.BOARD_SIZE - self.width + 1
    
    def rotate_matrix_to(self, end_state):        
        while(self.rotation_state != end_state):
            self.rotate_matrix()
        
    def shift_right(self):
        self.position_state = (self.position_state + 1) % self.positions
        
    def print_tetromino(self):
        print("\nshape: ", self.shape)
        print("rotation state: ", self.rotation_state)
        print("position state: ", self.position_state)
        print("matrix: \n", self.matrix)
        
