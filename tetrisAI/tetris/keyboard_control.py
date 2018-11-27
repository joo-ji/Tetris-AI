import time
import numpy as np

from pynput import keyboard, mouse
from PIL import ImageGrab

from tetris_ai import Tetris_AI
from tetromino import Tetromino

print("Start Tetris AI")

# initialized Tetris AI
dumb_robot = Tetris_AI()

# program begins running when user clicks the play button
def on_click(x, y, button, pressed):
    if not pressed:
        return False
    
with mouse.Listener(
        on_click = on_click) as listener:
    listener.join()

time.sleep(4)

start_time = time.time()
elapsed_time = 0
#counter = 0

key_controller = keyboard.Controller()

# first Tetromino is fast dropped in place
img = ImageGrab.grab(bbox=(739, 292, 754, 307))
img_np = np.array(img)
img.save('tetromino_image.png')
tetro_color = tuple(img_np[14, 14])
input_tetro = Tetromino(tetro_color)
dumb_robot.playgrid.fast_drop(input_tetro)
dumb_robot.print_self()
counter = 0

while(True):
    img = ImageGrab.grab(bbox=(739, 292, 754, 307))
    img.save('tetromino_image1.png')
    img_np = np.array(img)
    
    if(tetro_color == tuple(img_np[14, 14]) or tuple(img_np[14, 14]) == (43, 43, 43)):
        key_controller.press(keyboard.Key.space)
        time.sleep(0.05)
        key_controller.release(keyboard.Key.space)
    
    else:
        counter += 1
        dumb_robot.print_self()
        #print(counter)
        tetro_color = tuple(img_np[14, 14])
        input_tetro = Tetromino(tetro_color)
        game_tetro = Tetromino(tetro_color)
        #print(input_tetro.matrix)
        pos, rots = dumb_robot.run_ai(input_tetro)
        #need to shift I blocks if rotating
        while(game_tetro.rotation_state != rots):
            time.sleep(0.1)
            key_controller.press(keyboard.Key.up)
            time.sleep(0.04)
            key_controller.release(keyboard.Key.up)
            #keyboard.press('u')
            #keyboard.release('u')
            game_tetro.rotate_matrix()
        
        print(game_tetro.matrix)
        print("rotation: ", game_tetro.rotation_state)
        print("desired rotation: ", rots)
        while(game_tetro.position_state != pos):
            time.sleep(0.15)
            if(game_tetro.position_state > pos):
                key_controller.press(keyboard.Key.left)
                time.sleep(0.05)
                key_controller.release(keyboard.Key.left)
                game_tetro.position_state -= 1
            else:
                key_controller.press(keyboard.Key.right)
                time.sleep(0.05)
                key_controller.release(keyboard.Key.right)
                game_tetro.position_state += 1
            #keyboard.press('r')
            #keyboard.release('r')
        print("position: ", game_tetro.position_state)
        print("desired position: ", pos)
        