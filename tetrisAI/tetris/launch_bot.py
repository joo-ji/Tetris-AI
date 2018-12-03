import time

from pynput import keyboard

import input_controls as controls
from tetris_ai import Tetris_AI
from tetromino import Tetromino

print("Start Tetris AI")

# initialized Tetris AI
dumb_robot = Tetris_AI()

# program begins running when user clicks the play button
def on_press(key):
    if(key == keyboard.Key.space):
        tetro_color = controls.capture_tetromino()
        input_tetro = Tetromino(tetro_color)
        dumb_robot.playgrid.fast_drop(input_tetro)
        dumb_robot.print_self()
        
        return False
    
with keyboard.Listener(
        on_press = on_press) as listener:
    listener.join()

start_time = time.time()
elapsed_time = 0

key_controller = keyboard.Controller()

while(time.time() - start_time <= 120):
    tetro_color = controls.capture_tetromino()
    
    if(tetro_color != (43, 43, 43)):
        if(dumb_robot.hold_tetromino(tetro_color)):
            controls.hold_controller()
            tetro_color = controls.capture_tetromino()
            
        if(dumb_robot.clear_mode(tetro_color)):
            print("CLEAR MODE")
            input_tetro = Tetromino(tetro_color)
            game_tetro = Tetromino(tetro_color)
            
            positions, rotations, fit_score, fit_array = dumb_robot.run_ai(input_tetro, True)
            dumb_robot.print_self()
            
            controls.rotation_controller(game_tetro, rotations)
            controls.translation_controller(game_tetro, positions)
            controls.fast_drop_controller()
            
            time.sleep(0.15)
            
            tetro_color = controls.capture_tetromino()
            dumb_robot.hold_piece = Tetromino(tetro_color)
            
            controls.hold_controller()
            
            positions, rotations, fit_score, fit_array = dumb_robot.run_ai(input_tetro, True)
            dumb_robot.print_self()
            
            controls.rotation_controller(game_tetro, rotations)
            controls.translation_controller(game_tetro, positions)
            controls.fast_drop_controller()
            
            tetro_color = controls.capture_tetromino()
        
        input_tetro = Tetromino(tetro_color)
        game_tetro = Tetromino(tetro_color)
        
        positions, rotations, fit_score, fit_array = dumb_robot.run_ai(input_tetro, False)
        dumb_robot.print_self()
        
        print("fitness score: ", fit_score)
        print("[clear_factor, holes, h_level, h_diff]\n", fit_array)
            
        controls.rotation_controller(game_tetro, rotations)
            
        print(game_tetro.matrix)
        #print("rotation: ", game_tetro.rotation_state)
        #print("desired rotation: ", rotations)
        
        controls.translation_controller(game_tetro, positions)
        
        #print("position: ", game_tetro.position_state)
        #print("desired position: ", positions)
        
        controls.fast_drop_controller()
        