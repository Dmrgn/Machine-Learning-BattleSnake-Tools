from pyray import *
import random
import tensorflow as tf
import numpy as np

from constants import *
from formatBoard import format_board

model = tf.keras.models.load_model('dense.h5')
COLS = [GREEN, BLUE, PINK, YELLOW, ORANGE, PURPLE]

class Snake:
    def __init__(self, x, y, id):
        self.x = x
        self.y = y
        self.id = id
        self.tail = []
        self.color = random.choice(COLS)
        self.is_dead = False
        for x in range(2):
            self.tail.append({"x": self.x, "y": self.y})
    def update(self, snakes, food):
        # update tail pos
        for i in reversed(range(len(self.tail))):
            if i == 0:
                continue
            self.tail[i]["x"] = self.tail[i-1]["x"]
            self.tail[i]["y"] = self.tail[i-1]["y"]
        self.tail[0]["x"] = self.x
        self.tail[0]["y"] = self.y
        # prompt network for a move
        alive_snakes = list(filter(lambda s: not s.is_dead, snakes))
        input = np.array(format_board(self, alive_snakes, food)).reshape(1, 11, 11, 3)
        # input = np.array(format_board(self, alive_snakes, food)).reshape(1, 363) # for dense nn
        prediction = list(model.predict(input, verbose=0)[0])
        # make sure the move isnt terrible
        possibles = [{"index": i, "value": prediction[i]} for i in range(len(prediction))]
        possibles.sort(key=lambda a: a["value"])
        best = possibles.pop()
        while self.is_a_terrible_move(alive_snakes, best):
            if len(possibles) == 0:
                best = None
                break
            best = possibles.pop()
        # if all moves are terrible (sadge) then use whatever the nn says
        if best is None:
            dir = DIRS[prediction.index(max(prediction))]
        # otherwise use the best move
        else:
            dir = DIRS[best["index"]]
        self.x += dir["x"]
        self.y += dir["y"]
        # check if we are eating food
        for piece in food:
            if self.x == piece["x"] and self.y == piece["y"]:
                food.remove(piece)
                self.tail.append({"x": self.tail[len(self.tail)-1]["x"], "y": self.tail[len(self.tail)-1]["y"]})
    # terrible moves immediately kill us
    def is_a_terrible_move(self, snakes, best):
        best_dir = DIRS[best["index"]]
        new_x = self.x + best_dir["x"]
        new_y = self.y + best_dir["y"]
        for snake in snakes:
            for piece in snake.tail:
                if new_x == piece["x"] and new_y == piece["y"]:
                    return True
        return False
    def should_be_dead(self, snakes):
        # check if we are dead
        tail_poses = []
        for snake in snakes:
            if snake.is_dead:
                continue
            for piece in snake.tail:
                tail_poses.append(piece)
            if snake.id != self.id:
                tail_poses.append({"x": snake.x, "y": snake.y})
        for piece in tail_poses:
            if self.x == piece["x"] and self.y == piece["y"]:
                self.is_dead = True
                return
        if self.x < 0 or self.y < 0 or self.x >= BOARD_WIDTH or self.y >= BOARD_HEIGHT:
            self.is_dead = True
            return
    def draw(self):
        draw_rectangle(int(self.x*GS_WIDTH), int(self.y*GS_HEIGHT), int(GS_WIDTH), int(GS_HEIGHT), color_alpha(self.color, 0.8))
        for piece in self.tail:
            draw_rectangle(int(piece["x"]*GS_WIDTH), int(piece["y"]*GS_HEIGHT), int(GS_WIDTH), int(GS_HEIGHT), self.color)
    def draw_dead(self):
        draw_rectangle(int(self.x*GS_WIDTH), int(self.y*GS_HEIGHT), int(GS_WIDTH), int(GS_HEIGHT), color_alpha(self.color, 0.2))
        for piece in self.tail:
            draw_rectangle(int(piece["x"]*GS_WIDTH), int(piece["y"]*GS_HEIGHT), int(GS_WIDTH), int(GS_HEIGHT), color_alpha(self.color, 0.2))