import msgpack
import json
import gc

# channel [0] == food
# channel [1] == winner snake
# channel [2] == other snakes

DIRS = [
    {"X":-1, "Y":0}, # left
    {"X":0, "Y":-1}, # up
    {"X":1, "Y":0}, # right
    {"X":0, "Y":1}, # down
]

# with open('sampleGame.json', 'r') as f:
#     data = json.load(f)

with open('finaldata/data.msgpack', 'rb') as f:
    data = msgpack.load(f)

def preprocessGame(game, flip=False):
    frames = []
    X = "Y" if flip else "X"
    Y = "X" if flip else "Y"
    for i in range(len(game["states"])-1):
        # get which direction was chosen after this state
        headPosThisFrame = list(filter(lambda snake: snake["id"] == game["winnerId"], game["states"][i]["snakes"]))[0]["body"][0]
        headPosNextFrame = list(filter(lambda snake: snake["id"] == game["winnerId"], game["states"][i+1]["snakes"]))[0]["body"][0]
        dir = {"X": headPosNextFrame[X]-headPosThisFrame[X], "Y": headPosNextFrame[Y]-headPosThisFrame[Y]}
        dirIndex = DIRS.index(dir)
        # one-hot encode the dirIndex
        encodedDir = [0, 0, 0, 0]
        encodedDir[dirIndex] = 1
        # convert snake info to 2d board array
        board = []
        for j in range(11):
            board.append([])
            for k in range(11):
                board[j].append([])
                for l in range(3):
                    board[j][k].append(0)
        # add snakes
        for snake in game["states"][i]["snakes"]:
            if snake["id"] == game["winnerId"]:
                # manually set snake head
                board[snake["body"][0][X]][snake["body"][0][Y]][1] = 5
                # set other pieces
                for j in range(len(snake["body"])-1):
                    board[snake["body"][j+1][X]][snake["body"][j+1][Y]][1] = 1
            else:
                # manually set snake head
                board[snake["body"][0][X]][snake["body"][0][Y]][2] = 5
                # set other pieces
                for j in range(len(snake["body"])-1):
                    board[snake["body"][j+1][X]][snake["body"][j+1][Y]][2] = 1
        # add food
        for food in game["states"][i]["food"]:
            board[food[X]][food[Y]][0] = 1
        frames.append({
            "input":board,
            "output":encodedDir
        })
    return frames

preprocessed = []
num = 0
for game in data:
    # preprocessedGame = preprocessGame(game)
    # for frame in preprocessedGame:
    #     preprocessed.append(frame)
    preprocessedFlippedGame = preprocessGame(game, True)
    for frame in preprocessedFlippedGame:
        preprocessed.append(frame)
    print("Game", num, ": Number of frames", len(preprocessed))
    num+=1

with open('data/preprocessed_data.msgpack', 'wb') as f:
    msgpack.dump(preprocessed, f)