import numpy as np

from tetromino import Tetromino
from playfield import Playfield
from tetris_ai import Tetris_AI

A = np.array([[1,1,1,1,1],[1,1,1,1,1],[1,1,1,1,1]])
print(len(A))
print(len(A[:,1]))
print(len(A[1,:]))

a = np.arange(20).reshape((5,4))
# array([[ 0,  1,  2,  3],
#        [ 4,  5,  6,  7],
#        [ 8,  9, 10, 11],
#        [12, 13, 14, 15],
#        [16, 17, 18, 19]])

# If I select certain rows, it works
print (a[:,0:2])
#[[ 0  1]
# [ 4  5]
# [ 8  9]
# [12 13]
# [16 17]]

# If I select certain rows and a single column, it works
#print a[[0, 1, 3], 2]
# array([ 2,  6, 14])

# But if I select certain rows AND certain columns, it fails
#print a[[0,1,3], [0,2]]
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# ValueError: shape mismatch: objects cannot be broadcast to a single shape


#a = np.array([0,0,4,4,4,4,2,2,2,2])
#b = a[::-1]
#i = len(b) - np.argmax(b) - 1
#i     # 5
#a[i:] # array([4, 2, 2, 2, 2])



tetromino_L = Tetromino('L')
tetromino_L.print_tetromino()


playfield_test = Playfield()
print(playfield_test.grid)

print("add L rotated once")
print(playfield_test.fast_drop(tetromino_L))

print("add another L")
print(playfield_test.fast_drop(Tetromino('O')))

print("add another L")
print(playfield_test.fast_drop(Tetromino('O')))

print("add another L")
test = Tetromino('O')
print("L block positions\n", test.positions)
test.rotate_matrix()
print("L block positions\n", test.positions)
print(playfield_test.fast_drop(test))

print("add another L")
test2 = Tetromino('O')
test2.shift_right()
playfield_test.fast_drop(test2)

print("\n\nother test\n")
playfield_test.update_block_height()
#playfield_test.test_time()

print(playfield_test.combo)
print(playfield_test.should_clear())

ai = Tetris_AI()
print(ai.time_test())