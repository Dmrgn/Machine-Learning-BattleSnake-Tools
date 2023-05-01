from websocket import create_connection
import json

# current websocket connection
ws = {"isInited":False, "connection":None}

game_id_global = None

def create_ws_connection(game_id):
    if ws["isInited"]:
        print("Attempted to create a websocket connection, but one is already connected.")
        return False
    global game_id_global
    game_id_global = game_id
    ws["connection"] = create_connection("wss://engine.battlesnake.com/games/{}/events".format(game_id))
    ws["isInited"] = True
    return True

def read_ws_next_response():
    if not ws["isInited"]:
        print("Attempted to read data from websocket, but no websocket is connected.")
        return False
    try:
        response = ws["connection"].recv()
        return json.loads(response)
    except:
        print("Failed to read websocket response")
        ws["connection"].close()
        ws["isInited"] = False
    return False

def close_ws_connection():
    ws["connection"].close()
    ws["isInited"] = False