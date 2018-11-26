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
input_tetro = Tetromino(tuple(img_np[14, 14]))
dumb_robot.playgrid.fast_drop(input_tetro)
dumb_robot.print_self()

def on_press(key):

    if(key == keyboard.Key.space):
        print("PLEASE")
        img = ImageGrab.grab(bbox=(739, 292, 754, 307))
        img.save('tetromino_image.png')
        img_np = np.array(img) 
        input_tetro = Tetromino(tuple(img_np[14, 14]))
        pos, moves, rots = dumb_robot.run_ai(input_tetro)
        while(moves > 0):                
            if(input_tetro.position_state < pos):
                key_controller.press(keyboard.Key.left)
                key_controller.release(keyboard.Key.left)
            else:
                key_controller.press(keyboard.Key.right)
                key_controller.release(keyboard.Key.right)
            #keyboard.press('r')
            #keyboard.release('r')
            moves -= 1
    
        while(rots > 0):
            key_controller.press(keyboard.Key.up)
            key_controller.release(keyboard.Key.up)
            #keyboard.press('u')
            #keyboard.release('u')
            rots -= 1
        
        key_controller.press(keyboard.Key.space)
        key_controller.release(keyboard.Key.space)
        dumb_robot.print_self()
    elif(key == keyboard.Key.esc):
        return False

with keyboard.Listener(
        on_press = on_press) as listener:
    listener.join()
