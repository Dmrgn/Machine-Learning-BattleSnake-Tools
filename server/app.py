from flask import *

from snake import Snake

app = Flask(__name__)

snake = Snake()

DIRS = [
    "left",
    "down",
    "right",
    "up"
]

@app.route("/", methods=['GET'])
def main():
    return jsonify({
        "apiversion": "1",
        "author": "danielisokayig",
        "color": "#FF0000",
        "head": "fang",
        "tail": "bolt",
        "version": "0.0.1-beta"
    })

@app.route("/start", methods=['POST'])
def start():
    return ""

@app.route("/move", methods=['POST'])
def move():
    content = request.json
    id = content["you"]["id"]
    snakes = [x for x in content["board"]["snakes"]]
    food = [x for x in content["board"]["food"]]
    return jsonify({
        "move": DIRS[snake.update(id, snakes, food)],
        "shout": "In the fog of great chaos shines the light of great opportunity."
    })

@app.route("/end", methods=['POST'])
def end():
    return ""