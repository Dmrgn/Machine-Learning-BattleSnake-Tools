import tensorflow as tf
import numpy as np

from formatBoard import format_board

model = tf.keras.models.load_model('big3.h5')

DIRS = [
    {"x": -1, "y": 0}, # left
    {"x": 0, "y": -1}, # down
    {"x": 1, "y": 0}, # right
    {"x": 0, "y": 1}, # up
]

class Snake:
    def is_a_terrible_move(self, snakes, this_snake_x, this_snake_y, best):
        best_dir = DIRS[best["index"]]
        new_x = this_snake_x + best_dir["x"]
        new_y = this_snake_y + best_dir["y"]
        if new_x > 10 or new_x < 0 or new_y > 10 or new_y < 0:
            return True
        for snake in snakes:
            for piece in snake["body"]:
                if new_x == piece["x"] and new_y == piece["y"]:
                    print("terrible move", this_snake_x, this_snake_y, new_x, new_y)
                    return True
        return False
    def update(self, id, snakes, food):
        # set our position
        this_snake = list(filter(lambda snake: snake["id"] == id, snakes))[0]
        this_snake_x = int(this_snake["head"]["x"])
        this_snake_y = int(this_snake["head"]["y"])
        # update head pos
        input = np.array(format_board(id, snakes, food)).reshape(1, 11, 11, 3)
        prediction = list(model.predict(input)[0])
        print(prediction)
        # make sure the move isnt terrible
        possibles = [{"index": i, "value": prediction[i]} for i in range(len(prediction))]
        possibles.sort(key=lambda a: a["value"])
        best = possibles.pop()
        while self.is_a_terrible_move(snakes, this_snake_x, this_snake_y, best):
            if len(possibles) == 0:
                best = None
                break
            best = possibles.pop()
        # if all moves are terrible (sadge) then use whatever the nn says
        if best is None:
            return prediction.index(max(prediction))
        # otherwise use the best move
        return best["index"]