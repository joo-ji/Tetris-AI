import time

from pynput import keyboard

import config as cfg
import input_controls as controls
import tetris_sim as sim
from tetromino import Tetromino
from playfield import Playfield

print("Start Tetris AI")

# initialize playgrid
playgrid = Playfield()

# program begins running when user clicks the play button
def on_press(key):
    if(key == keyboard.Key.space):
        tetro_color = controls.capture_tetromino()
        input_tetro = Tetromino(color=tetro_color)
        playgrid.fast_drop(input_tetro)
        playgrid.print_self()
        return False

with keyboard.Listener(
        on_press = on_press) as listener:
    listener.join()

start_time = time.time()
elapsed_time = 0

key_controller = keyboard.Controller()

while(time.time() - start_time <= 120):
    time.sleep(0.05)
    tetro_color = controls.capture_tetromino()

    if(tetro_color != (43, 43, 43) or tetro_color != (255, 255, 255)):

        sim_tetro = Tetromino(color=tetro_color)
        input_tetro = Tetromino(color=tetro_color)
        positions, rotations, fit_score, fit_array = sim.run(sim_tetro, playgrid, cfg.TEST_WEIGHTS)

        controls.rotation_controller(input_tetro, rotations)
        controls.translation_controller(input_tetro, positions)
        controls.fast_drop_controller()

        if(playgrid.lines_cleared != 0):
            time.sleep(0.25)

        print(input_tetro.matrix)
        playgrid.print_self()
        print("fitness score: ", fit_score)
        print("parameter array: ", fit_array)
