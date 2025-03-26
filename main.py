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
start_time = round(time.time())
save_time = start_time
hunger = 4
happy = 4
discipline = 0
weight = 1
poo = 0
sick = False
teen_ver = 1 # will be randomly set between [1,2] for new games
adult_ver = 1 # will be randomly set between [1,6] for new games
dead = False
want_attention = False
asleep = False

# check if there is a save file, if not create one, and if there is load data into tamagotchi variables
if not os.path.exists(GC.SAVE_FILE):
    with open(GC.SAVE_FILE, "w") as save_file:
        json.dump(save_data(age, start_time, save_time, hunger, happy, discipline, weight, poo, sick, teen_ver, adult_ver, dead, want_attention, asleep),
                  save_file, indent=4)
else:
    with open(GC.SAVE_FILE, "r") as save_file:
        game_save = json.load(save_file)
        age = game_save["age"]
        start_time = game_save["start_time"]
        save_time = game_save["save_time"]
        hunger = game_save["hunger"]
        happy = game_save["happy"]
        discipline = game_save["discipline"]
        weight = game_save["weight"]
        poo = game_save["poo"]
        sick = game_save["sick"]
        teen_ver = game_save["teen_ver"]
        adult_ver = game_save["adult_ver"]
        dead = game_save["dead"]
        want_attention = game_save["want_attention"]
        asleep = game_save["asleep"]

# pygame setup
pygame.init()
# initialize display
WIDTH, HEIGHT = 1280, 720
display = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('~Tamagotchi Recreated~')
# game loop variables
FPS = 60
clock = pygame.time.Clock()
run = True
# game images
btn_images = disp_func.get_btn_images()
stage_images = disp_func.get_stage_images(teen_ver, adult_ver)

# game loop
while run:
    clock.tick(FPS)

    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # handle saving game here
            run = False

    # render game here

    # temp display
    display.fill("white")
    display.blit(stage_images['adult_spec'], (250, 100))
    pygame.display.update()

# close program
pygame.quit()