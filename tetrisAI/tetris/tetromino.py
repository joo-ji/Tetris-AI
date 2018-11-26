import numpy as np

class Tetromino:
    TETROMINO_TYPE = {
            (44, 209, 255):(
                    'I',
                    2,
                    np.array(
                            [[1, 1, 1, 1]],
                             )
                ),
            (68, 124, 255):(
                    'J',
                    4,
                    np.array(
                            [[1, 0, 0],
                             [1, 1, 1]],
                            )
                ),
            (255, 156, 35):(
                    'L',
                    4,
                    np.array(
                            [[0, 0, 1],
                             [1, 1, 1]],
                             )
                ),
            (255, 217, 59):(
                    'O',
                    1,
                    np.array(
                            [[1, 1],
                             [1, 1]],
                            )
                ),
            (134, 234, 51):(
                    'S',
                    4,
                    np.array(
                            [[0, 1, 1],
                            [1, 1, 0]],
                            )
                ),
            (232, 76, 201):(
                    'T',
                    4,
                    np.array(
                            [[0, 1, 0],
                             [1, 1, 1]],
                            )
                ),
            (255, 67, 92):(
                    'Z',
                    4,
                    np.array(
                            [[1, 1, 0],
                             [0, 1, 1]],
                            )
                )
    }
    
    SPAWN_POSITION = 3
    BOARD_SIZE = 10
    
    def __init__(self, color):
        self.color = color
        self.rotation_state = 0
        self.create_Tetromino()
        
        self.position_state = self.SPAWN_POSITION
        if(self.shape == 'O'):
            self.position_state += 1
        
        
    def create_Tetromino(self):
        self.shape, self.rotations, self.matrix = self.TETROMINO_TYPE[self.color]
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
        rotations = 0
        while(self.rotation_state != end_state):
            self.rotate_matrix()
            rotations += 1
            
        return rotations
        
    def shift_right(self):
        self.position_state = (self.position_state + 1) % self.positions
    
    def shift_right_to(self, end_state):
        moves = 0
        while(self.position_state != end_state):
            self.shift_right()
            moves += 1
            
        return moves
    
    def print_tetromino(self):
        print("\nshape: ", self.shape)
        print("rotation state: ", self.rotation_state)
        print("position state: ", self.position_state)
        print("matrix: \n", self.matrix)
        
