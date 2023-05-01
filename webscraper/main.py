import snakeCatcher
import msgpack

data = [] # all data in the database
used_snakes = set() # cache of snakes which have already been used
used_games = set() # cache of games which have already been used
snake_ids = snakeCatcher.fetch_snakes_from_leaderboard() # list of all snake ids currently on the leaderboard
num_snakes_processed = 0 # number of snakes processed this session
cutoff = 0.10 # only get data on the top n percent of the snakes

def save():
    with open('newdata/used_games.msgpack', 'wb') as f:
        f.write(msgpack.dumps(list(used_games)))
    with open('newdata/used_snakes.msgpack', 'wb') as f:
        f.write(msgpack.dumps(list(used_snakes)))
    with open('newdata/data.msgpack', 'wb') as f:
        f.write(msgpack.dumps(data))
def load():
    global used_games
    global used_snakes 
    global data
    with open('data/used_games.msgpack', 'rb') as f:
        used_games = set(msgpack.loads(f.read()))
    with open('data/used_snakes.msgpack', 'rb') as f:
        used_snakes = set(msgpack.loads(f.read()))
    with open('data/data.msgpack', 'rb') as f:
        data = msgpack.loads(f.read())

# load()

print("Found", len(snake_ids), "snakes on the leaderboard.")
snake_ids = snake_ids[:round(len(snake_ids)*cutoff)]
print("Taking top", len(snake_ids), "snakes on the leaderboard for processing.")
for snake_id in snake_ids:
    print("\tProcessing snake (", num_snakes_processed,"/",len(snake_ids), ") with id", snake_id)
    if not snake_id in used_snakes:
        num_games_processed = 0
        for game_id in snakeCatcher.fetch_snake_recent_games(snake_id):
            print("\t\tProcessing game", num_games_processed, "with id", game_id)
            if not game_id in used_games:
                game_data = snakeCatcher.fetch_game_data(game_id)
                if game_data == False:
                    print("\t\tError processing game", num_games_processed, "with id", game_id, "skipped.")
                else:
                    data.append(game_data)
                    num_games_processed += 1
                used_games.add(game_id)
            else:
                print("\t\tGame skipped as it already exists in the database.")
        print("\tCompleted snake", num_snakes_processed)
        print("\tData size", len(data))
        print("\tData saved to file.")
        used_snakes.add(snake_id)
        num_snakes_processed += 1
        save()
    else:
        print("\tSnake skipped as it already exists in the database.")