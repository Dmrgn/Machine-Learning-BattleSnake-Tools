from constants import *

def format_board(snake, snakes, food):
    # convert snake info to 2d board array
    board = []
    for j in range(11):
        board.append([])
        for k in range(11):
            board[j].append([])
            for l in range(3):
                board[j][k].append(0)
    # add snakes
    for s in snakes:
        if s.id == snake.id:
            continue
        board[s.tail[0]["x"]][s.tail[0]["y"]][2] = 5
        for j in range(len(s.tail)-1):
            board[s.tail[j+1]["x"]][s.tail[j+1]["y"]][2] = 1
    # add this snake
    board[snake.tail[0]["x"]][snake.tail[0]["y"]][1] = 5
    for j in range(len(snake.tail)-1):
        board[snake.tail[j+1]["x"]][snake.tail[j+1]["y"]][1] = 1
    # add food
    for f in food:
        board[f["x"]][f["y"]][0] = 1
    return board