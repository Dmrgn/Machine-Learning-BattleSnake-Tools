import msgpack
import numpy as np

DIRS = [
    {"X":-1, "Y":0}, # left
    {"X":0, "Y":-1}, # up
    {"X":1, "Y":0}, # right
    {"X":0, "Y":1}, # down
]

SOURCES = 3

def rotateFrame(frame):
    # rotate the input array
    rotated_array = np.rot90(np.array(frame["input"])).tolist()
    # rotate the output direction
    dir_index = frame["output"].index(1)
    dir_index += 1 # rotation counter clockwise 90 degrees
    dir_index %= 4
    # one hot encode output direction
    rotated_dir = [0,0,0,0]
    rotated_dir[dir_index] = 1
    return {
        "input": rotated_array,
        "output": rotated_dir
    }


for source in range(SOURCES):
    with open('data/{}.msgpack'.format(source), 'rb') as f:
        data = msgpack.load(f)
    for dir in range(3):
        preprocessed = []
        for frame in data:
            rotated_frame = frame
            for x in range(dir+1):
                rotated_frame = rotateFrame(rotated_frame)
            preprocessed.append(rotateFrame(frame))
            print("Source", source, "Rotation", dir, "Number of frames", len(preprocessed))
        with open('data/{}.msgpack'.format(SOURCES+source*3+dir), 'wb') as f:
            msgpack.dump(preprocessed, f)

    # [
    #     [[0, 1, 0], [0, 0, 1], [0, 1, 0]],
    #     [[0, 1, 0], [0, 0, 0], [0, 1, 0]],
    #     [[1, 0, 1], [1, 0, 0], [0, 0, 0]]
    # ]

    # [
    #     [[0, 1, 0], [0, 1, 0], [0, 0, 0]],
    #     [[0, 0, 1], [0, 0, 0], [1, 0, 0]],
    #     [[0, 1, 0], [0, 1, 0], [1, 0, 1]]
    # ]