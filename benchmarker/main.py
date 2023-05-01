import random
import uuid
import json
from pyray import *

from snake import Snake
from constants import *

snakes = []
food = []
turn = 0
snake_lengths = []
benchmark_data = []

if IS_GRAPHICAL:
    init_window(800, 800, "Snake")
    set_target_fps(FRAME_RATE)

def start_game():
    global food, snakes, turn, snake_lengths
    snakes = [Snake(loc["x"], loc["y"], uuid.uuid1()) for loc in SPAWN_LOCS]
    food = []
    turn = 0
    num_snakes_remaining = 4
    for snake in snakes:
        selection = random.choice(FOOD_LOCS)
        food_pos = {"x": selection["x"], "y": selection["y"]}
        food_pos["x"] += snake.x
        food_pos["y"] += snake.y
        food.append(food_pos)
    food.append({"x":int(BOARD_WIDTH/2), "y":int(BOARD_HEIGHT/2)})
    while not((window_should_close() if (IS_GRAPHICAL) else False) or num_snakes_remaining == 1):
        if IS_GRAPHICAL:
            begin_drawing()
            clear_background(GRAY)
        turn+=1
        snake_lengths = []
        # update snakes
        num_snakes_remaining = 0
        for snake in snakes:
            snake_lengths.append(len(snake.tail)+1)
            if not snake.is_dead:
                num_snakes_remaining += 1
                snake.update(snakes, food)
        for snake in snakes:
            snake.should_be_dead(snakes)
        if IS_GRAPHICAL:
            # draw snakes
            for snake in snakes:
                if not snake.is_dead:
                    snake.draw()
                else:
                    snake.draw_dead()
            # draw food
            for f in food:
                draw_ellipse(int(f["x"]*GS_WIDTH+GS_WIDTH/2), int(f["y"]*GS_HEIGHT+GS_HEIGHT/2), int(GS_WIDTH/2), int(GS_HEIGHT/2), RED)
        # spawn food
        if random.randint(1, 8) == 1:
            pos = {"x": 0, "y": 0}
            is_good_pos = False
            while not is_good_pos:
                is_good_pos = True
                pos["x"] = random.randint(0, BOARD_WIDTH-1)
                pos["y"] = random.randint(0, BOARD_WIDTH-1)
                for snake in snakes:
                    if not snake.is_dead:
                        for piece in snake.tail:
                            if pos["x"] == piece["x"] and pos["y"] == piece["y"]:
                                is_good_pos = False
            food.append(pos)
        if IS_GRAPHICAL:
            end_drawing()
    if IS_GRAPHICAL:
        if window_should_close():
            return

for x in range(NUM_BENCHMARKS):
    print("Benchmarking game", x+1, "/", NUM_BENCHMARKS)
    start_game()
    print("\tturns:", turn, "lengths", snake_lengths)
    benchmark_data.append({
        "turns": turn,
        "lengths": snake_lengths 
    })

with open("benchmark_data.json", "w") as f:
    json.dump(benchmark_data, f)

if IS_GRAPHICAL:
    close_window()