import time
import numpy as np

from pynput import keyboard
from PIL import ImageGrab

def capture_tetromino():
    #img = ImageGrab.grab(bbox=(739, 320, 754, 335))
    img = ImageGrab.grab(bbox=(672, 365, 692, 385))
    img.save('tetromino_image.png')
    img_np = np.array(img)
    return tuple(img_np[10, 10])

key_controller = keyboard.Controller()

def translation_controller(game_tetro, position):
    while(game_tetro.position_state != position):
        time.sleep(0.12)
        if(game_tetro.position_state > position):
            key_controller.press(keyboard.Key.left)
            time.sleep(0.05)
            key_controller.release(keyboard.Key.left)
            game_tetro.position_state -= 1
        else:
            key_controller.press(keyboard.Key.right)
            time.sleep(0.05)
            key_controller.release(keyboard.Key.right)
            game_tetro.position_state += 1

def rotation_controller(game_tetro, rotation):
    while(game_tetro.rotation_state != rotation):
        time.sleep(0.12)
        key_controller.press(keyboard.Key.up)
        time.sleep(0.05)
        key_controller.release(keyboard.Key.up)
        game_tetro.rotate_clockwise()
    return game_tetro

def hold_controller():
    key_controller.press(keyboard.Key.shift_l)
    time.sleep(0.05)
    key_controller.release(keyboard.Key.shift_l)

def fast_drop_controller():
    key_controller.press(keyboard.Key.space)
    time.sleep(0.05)
    key_controller.release(keyboard.Key.space)
