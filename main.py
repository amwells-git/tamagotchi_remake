import pygame
import time
import json
import os
import random

from pygame.examples.moveit import WIDTH, HEIGHT

# import game constants
from src import game_constants as GC
# import save data function
from src.save_data import save_data
# import display functions
from src import display_functions as disp_func

# tamagotchi variables
age = 0
stage = "egg"
start_time = round(time.time())
elapsed_time = 0
save_time = start_time
hunger = 4
happy = 4
discipline = 0
weight = 1
poo = 0
last_poo = start_time
sick = 0
teen_ver = 1 # will be randomly set between [1,2] for new games
adult_ver = 1 # will be randomly set between [1,6] for new games
dead = False
want_attention = False
current_wants = {}
asleep = False
sleep_start = 20 # will be randomly set between [18,23] for new games
sleep_end = 6 # will be randomly set between [0,8] for new games
light = True

# display variable to be changed by meter btn
# 0 is initial load / tamagotchi view
# 1 is show happy
# 2 is show hunger
# 3 is show discipline
# 4 is show age
current_display = 0

# check if there is a save file, if not create one, and if there is load data into tamagotchi variables
if not os.path.exists(GC.SAVE_FILE):
    with open(GC.SAVE_FILE, "w") as save_file:
        json.dump(save_data(age, stage, start_time, elapsed_time, save_time, hunger, happy, discipline, weight,
                            poo, last_poo, sick, teen_ver, adult_ver, dead, want_attention, current_wants, asleep,
                            sleep_start, sleep_end, light),
                  save_file, indent=4)
else:
    with open(GC.SAVE_FILE, "r") as save_file:
        game_save = json.load(save_file)
        age = game_save["age"]
        stage = game_save["stage"]
        start_time = game_save["start_time"]
        elapsed_time = game_save["elapsed_time"]
        save_time = game_save["save_time"]
        hunger = game_save["hunger"]
        happy = game_save["happy"]
        discipline = game_save["discipline"]
        weight = game_save["weight"]
        poo = game_save["poo"]
        last_poo = game_save["last_poo"]
        sick = game_save["sick"]
        teen_ver = game_save["teen_ver"]
        adult_ver = game_save["adult_ver"]
        dead = game_save["dead"]
        want_attention = game_save["want_attention"]
        current_wants = game_save["current_wants"]
        asleep = game_save["asleep"]
        sleep_start = game_save["sleep_start"]
        sleep_end = game_save["sleep_end"]
        light = game_save["light"]

# pygame setup
pygame.init()
# initialize display
display = pygame.display.set_mode((GC.WIDTH, GC.HEIGHT))
pygame.display.set_caption('~Tamagotchi Recreated~')
# game loop variables
FPS = 60
clock = pygame.time.Clock()
run = True
# game images
btn_images = disp_func.get_btn_images()
stage_images = disp_func.get_stage_images(teen_ver, adult_ver)
stat_images = disp_func.get_stat_images()

# define btn locations
btn_locations = {
    # top row
    "food": btn_images["food"].get_rect(topleft=GC.BTN_ROW_TOP),
    "light_off": btn_images["light_off"].get_rect(topleft=(2 * GC.BTN_ROW_TOP[0] - GC.BTN_GAP, GC.BTN_ROW_TOP[1])),
    "light_on": btn_images["light_on"].get_rect(topleft=(2 * GC.BTN_ROW_TOP[0] - GC.BTN_GAP, GC.BTN_ROW_TOP[1])),
    "game": btn_images["game"].get_rect(topleft=(3 * GC.BTN_ROW_TOP[0] - GC.BTN_GAP, GC.BTN_ROW_TOP[1])),
    "medicine": btn_images["medicine"].get_rect(topleft=(4 * GC.BTN_ROW_TOP[0] - GC.BTN_GAP, GC.BTN_ROW_TOP[1])),
    # bottom row
    "bathroom": btn_images["bathroom"].get_rect(topleft=GC.BTN_ROW_BOTTOM),
    "meter": btn_images["meter"].get_rect(topleft=(2 * GC.BTN_ROW_BOTTOM[0] - GC.BTN_GAP, GC.BTN_ROW_BOTTOM[1])),
    "discipline": btn_images["discipline"].get_rect(topleft=(3 * GC.BTN_ROW_BOTTOM[0] - GC.BTN_GAP, GC.BTN_ROW_BOTTOM[1])),
    "attention_wanted": btn_images["attention_wanted"].get_rect(topleft=(4 * GC.BTN_ROW_BOTTOM[0] - GC.BTN_GAP, GC.BTN_ROW_BOTTOM[1])),
    "attention_not_wanted": btn_images["attention_not_wanted"].get_rect(topleft=(4 * GC.BTN_ROW_BOTTOM[0] - GC.BTN_GAP, GC.BTN_ROW_BOTTOM[1])),
}
# define which buttons are active
active_btns = {"food", "light_off", "game", "medicine", "bathroom", "meter", "discipline", "attention_not_wanted"}
if want_attention:
    active_btns.remove("attention_not_wanted")
    active_btns.add("attention_wanted")
if not light:
    active_btns.clear()
    active_btns.add("light_on")
def normal_btns():
    global active_btns
    active_btns.clear()
    active_btns.add("food")
    active_btns.add("light_off")
    active_btns.add("game")
    active_btns.add("medicine")
    active_btns.add("bathroom")
    active_btns.add("meter")
    active_btns.add("discipline")
    if want_attention:
        active_btns.add("attention_wanted")
    else:
        active_btns.add("attention_not_wanted")

# btn event handler
def btn_event_handler(btn_name):
    # use global variables
    global hunger, happy, weight, discipline, poo, sick, current_wants, active_btns, light, current_display, dead

    if btn_name == "food":
        if hunger != 4:
            hunger = 4
        else: # considered a snack
            happy = max(4, happy + 1)
            weight += 2
    elif btn_name == "light_off":
        light = False
        active_btns.clear()
        active_btns.add("light_on")
    elif btn_name == "light_on":
        light = True
        active_btns.clear()
    elif btn_name == "game":
        # handle Higher Lower Game
        print("play game")
        weight = max(1, weight - 1)
    elif btn_name == "medicine":
        if sick > 0: sick - 1
        if "sick" in current_wants: current_wants.remove("sick")
    elif btn_name == "bathroom":
        poo = 0
    elif btn_name == "meter":
        if current_display == 4:
            current_display = 0
        else:
            current_display += 1
    elif btn_name == "discipline":
        if "false" in current_wants:
            discipline = max(4, discipline + 1)
            current_wants.remove("false")
    elif btn_name == "attention_wanted" or btn_name == "attention_not_wanted":
        if dead:
            print("Handle Creating A New Save")



# game loop
while run:
    clock.tick(FPS)

    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # handle saving game here
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for btn_name, btn_location in btn_locations.items():
                if btn_name in active_btns and btn_location.collidepoint(event.pos):
                    print(f"{btn_name} pressed")
                    btn_event_handler(btn_name)


    # render game here

    # temp display for testing
    display.fill("white")
    for btn_name, btn_location in btn_locations.items():
        if btn_name in active_btns:
            display.blit(btn_images[btn_name], btn_location.topleft)

    # update game display
    pygame.display.update()

# close program
pygame.quit()