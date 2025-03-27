# get common imports
from src.common_imports import *

# define save function using JSON
def save_game(game_data):
    with open(gc.SAVE_FILE, 'w') as save_file:
        json.dump(game_data, save_file, indent=4)

# define loading funciton
def load_game():
    if not os.path.exists(gc.SAVE_FILE):
        raise ValueError(f"{gc.SAVE_FILE} not found!")
    else:
        with open(gc.SAVE_FILE, 'r') as save_file:
            return json.load(save_file)

# function creates new game, saves it, then returns it
def new_game():
    # define NEW game data
    game_data = gc.GAME_INIT_DATA

    save_game(game_data)
    return game_data