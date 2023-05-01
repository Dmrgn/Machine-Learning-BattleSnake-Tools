from bs4 import BeautifulSoup as bs
import requests
import ws

LEADERBOARD_URL = "https://play.battlesnake.com/leaderboard/standard"
SNAKE_RECENT_GAMES_URL = "https://play.battlesnake.com/api/leaderboardsnake/{snake_id}/recent-games/"
GAME_DATA_URL = "wss://engine.battlesnake.com/games/{game_id}/events"

# fetch the ids of all the snakes on the current leaderboard
def fetch_snakes_from_leaderboard():
    leaderboard_soup = bs(requests.get(LEADERBOARD_URL).text, "html.parser") # get leaderboard soup
    snake_elements = leaderboard_soup.find_all(attrs={"data-snake-id": True}) # find all snakes
    snake_ids = [x.attrs["data-snake-id"] for x in snake_elements] # get the snakes' ids
    return snake_ids

# get the ids of the recently played games of the specified snake
def fetch_snake_recent_games(snake_id):
    recent_games = requests.get(SNAKE_RECENT_GAMES_URL.format(snake_id=snake_id)).json() # get recent games
    recent_games_ids = [x["gameId"] for x in recent_games["recentGames"]] # get the games' ids
    return recent_games_ids

# get board information for each turn of the specified game
def fetch_game_data(game_id):
    ws.create_ws_connection(game_id) # create websocket connection
    states = []
    winnerId = None
    response = ws.read_ws_next_response()
    if response == False: # if the game doesnt exist or a connection error occurs
        return False
    while response["Type"] != "game_end":
        # get list of alive snakes on the board (with only essential data)
        snakes = []
        for snake in response["Data"]["Snakes"]:
            if snake["Death"] == None:
                snakes.append({
                    "id": snake["ID"],
                    "body": snake["Body"],
                })
        # if there is one snake left, set it as the winner
        if len(snakes) == 1:
            winnerId = snakes[0]["id"]
        # add board state to the list
        states.append({
            "snakes": snakes,
            "food": response["Data"]["Food"],
        })
        # get next turn's board data
        response = ws.read_ws_next_response()
        # if the response failed, throw out this game or move on
        if response == False:
            if len(states) > 30:
                break
            else:
                print("Error processing websocket response, game too short")
                return False # exclude this game
    ws.close_ws_connection()
    # throw out game if there was no winner (2 died same frame etc...)
    if winnerId == None:
        print("Error, no winner")
        return False
    # return game data
    return {
        "states": states,
        "winnerId": winnerId 
    }