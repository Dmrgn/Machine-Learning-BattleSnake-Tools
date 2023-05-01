def format_board(id, snakes, food):
    # convert snake info to 2d board array
    board = []
    for j in range(11):
        board.append([])
        for k in range(11):
            board[j].append([])
            for l in range(3):
                board[j][k].append(0)
    # add snakes
    this_snake = None
    for s in snakes:
        if id == s["id"]:
            this_snake = s
            continue
        board[s["body"][0]["x"]][s["body"][0]["y"]][2] = 5
        for j in range(len(s["body"])-1):
            board[s["body"][j+1]["x"]][s["body"][j+1]["y"]][2] = 1
    # add this snake
    board[this_snake["body"][0]["x"]][this_snake["body"][0]["y"]][1] = 5
    for j in range(len(this_snake["body"])-1):
        board[this_snake["body"][j+1]["x"]][this_snake["body"][j+1]["y"]][1] = 1
    # add food
    for f in food:
        board[f["x"]][f["y"]][0] = 1
    return board