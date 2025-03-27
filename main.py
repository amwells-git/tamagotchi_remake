import pygame
import time
import datetime
import json
import os
import random

# import game constants
from src import game_constants as GC
# import save data function
from src.save_data import save_data
# import display functions
from src import image_load as img_load

# tamagotchi variables
age = 0
prev_age = 0
stage = "egg" # str from ["egg", "baby", "child", "teen", "adult", "adult_spec", "dead"]
start_time = round(time.monotonic())
elapsed_time = 0
save_time = time.time()
hunger = 4
last_hunger = elapsed_time
happy = 4
last_happy = elapsed_time
discipline = 0
weight = 1
poo = 0
last_poo = elapsed_time
sick = 0
teen_ver = 1 # will be randomly set between [1,2] for new games
adult_ver = 1 # will be randomly set between [1,6] for new games
dead = False
want_attention = False
current_wants = [] # {str,} each string is a specific want from ['hungry', 'unhappy', 'sick', 'sleepy', 'fake']
asleep = False
sleep_start = 20 # will be randomly set between [18,23] for new games
sleep_end = 6 # will be randomly set between [0,8] for new games
light = True
# if -1, that means timeout isn't active
wants_timeouts = {'hungry' : -1, 'unhappy' : -1, 'sick' : -1, 'sleepy' : -2, 'fake' : -1}

# display variable to be changed by meter btn
# 0 is initial load / tamagotchi view
# 1 is show happy
# 2 is show hunger
# 3 is show discipline
# 4 is show age
# 5 is show weight
current_display = 0
last_click = time.monotonic()
click_cooldown = 5

# save game function
def save_game():
    global age, prev_age, stage, start_time, elapsed_time, save_time, hunger, last_hunger, happy, last_happy, discipline, weight, poo, \
        last_poo, sick, teen_ver, adult_ver, dead, want_attention, current_wants, asleep, \
        sleep_start, sleep_end, light, wants_timeouts
    with open(GC.SAVE_FILE, "w") as save_file:
        json.dump(save_data(age, prev_age, stage, start_time, elapsed_time, save_time, hunger, last_hunger, happy, last_happy, discipline, weight,
                            poo, last_poo, sick, teen_ver, adult_ver, dead, want_attention, current_wants, asleep,
                            sleep_start, sleep_end, light, wants_timeouts),
                  save_file, indent=4)

# update the total game time for checks
def update_elapsed_time():
    global start_time, elapsed_time
    current_time = round(time.monotonic())
    elapsed_time += round(current_time - start_time)
    start_time = current_time

# check if there is a save file, if not create one, and if there is load data into tamagotchi variables
if not os.path.exists(GC.SAVE_FILE):
    save_game()
else:
    with open(GC.SAVE_FILE, "r") as save_file:
        game_save = json.load(save_file)
        age = game_save["age"]
        prev_age = game_save["prev_age"]
        stage = game_save["stage"]
        #start_time = round(time.monotonic()) # used to calculate elapsed time while program is running
        elapsed_time = game_save["elapsed_time"]
        save_time = game_save["save_time"]
        hunger = game_save["hunger"]
        last_hunger = game_save["last_hunger"]
        happy = game_save["happy"]
        last_happy = game_save["last_happy"]
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
        wants_timeouts = game_save["wants_timeouts"]

# pygame setup
pygame.init()
# initialize display
display = pygame.display.set_mode((GC.WIDTH, GC.HEIGHT))
pygame.display.set_caption('~Tamagotchi Recreated~')
# game loop variables
clock = pygame.time.Clock()
run = True
# game images
btn_images = img_load.get_btn_images()
stage_images = img_load.get_stage_images(teen_ver, adult_ver)
stat_images = img_load.get_stat_images()
# font
GAME_FONT = pygame.font.SysFont(GC.FONT_STYLE, GC.FONT_SIZE)

# define btn locations
btn_locations = {
    # top row
    "food": btn_images["food"].get_rect(topleft=GC.BTN_ROW_TOP),
    "light_off": btn_images["light_off"].get_rect(topleft=(2 * GC.BTN_ROW_TOP[0] - GC.BTN_GAP, GC.BTN_ROW_TOP[1])),
    "light_on": btn_images["light_on"].get_rect(topleft=(2 * GC.BTN_ROW_TOP[0] - GC.BTN_GAP, GC.BTN_ROW_TOP[1] + GC.BTN_SIZE + 10)),
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

def solve_wants(want=None):
    global current_wants, active_btns, wants_timeouts, elapsed_time, sick, discipline, want_attention
    # TODO: update elapsed time
    update_elapsed_time()

    # handle want timeout checks
    if want is None:
        for want in current_wants:
            if elapsed_time >= wants_timeouts[want] != -1:
                # TODO: Handle Care Mistake
                wants_timeouts[want] = -1
                current_wants.remove(want)
    else: # handle specific want
        if want in current_wants:
            current_wants.remove(want)
            wants_timeouts[want] = -1
            if want == "sick":
                sick = max(0, sick - 1)
            if want == "fake":
                discipline = max(4, discipline + 1)

    if not current_wants:
        want_attention = False

    # replace attention btn, only if light is on
    if 'attention_wanted' in active_btns and not want_attention and light:
        active_btns.remove('attention_wanted')
        active_btns.add('attention_not_wanted')
    elif 'attention_not_wanted' in active_btns and want_attention and light:
        active_btns.remove('attention_not_wanted')
        active_btns.add('attention_wanted')

def create_wants(want):
    global current_wants, active_btns, wants_timeouts, elapsed_time, sick, want_attention
    print(type(current_wants))
    # TODO: update elapsed time
    update_elapsed_time()

    if want not in current_wants:
        want_attention = True
        if want == "sick":
            sick = min(2, sick + 1)
        current_wants.append(want)
        wants_timeouts[want] = elapsed_time + GC.ATTENTION_TIMEOUT

    if want_attention and 'attention_wanted' not in active_btns:
        if 'attention_not_wanted' in active_btns:
            active_btns.remove('attention_not_wanted')
        active_btns.add('attention_wanted')

# btn event handler
def btn_event_handler(btn_name):
    # use global variables
    global hunger, happy, weight, poo, current_wants, active_btns, light, current_display, dead

    if btn_name == "food":
        if hunger != 4:
            solve_wants("hungry")
            hunger = 4
        else: # considered a snack
            happy = min(4, happy + 1)
            weight += 2
    elif btn_name == "light_off" or btn_name == "light_on":
        if light:
            solve_wants("sleepy")
            light = False
            # only show light_on btn
            active_btns.clear()
            active_btns.add("light_on")
        else:
            light = True
            # show normal btns
            normal_btns()
    elif btn_name == "game":
        # handle Higher Lower Game
        print("play game")
        solve_wants("unhappy")
        happy = min(4, happy + 1)
        weight = max(1, weight - 1)
    elif btn_name == "medicine":
        solve_wants("sick")
    elif btn_name == "bathroom":
        poo = 0
    elif btn_name == "meter":
        if current_display == 5:
            current_display = 0
        else:
            current_display += 1
    elif btn_name == "discipline":
        solve_wants("fake")
    elif btn_name == "attention_wanted" or btn_name == "attention_not_wanted":
        if dead:
            print("Handle Creating A New Save")

# game event handler (for timer based events)
def handle_timed_events():
    global stage, poo, last_poo, elapsed_time, age, asleep, wants_timeouts, prev_age, hunger, last_hunger, happy, last_happy, discipline
    update_elapsed_time()

    # handle stage time updates
    if stage != "egg" and stage != "dead":
        # handle baby stage specific updates
        if stage == "baby":
            if elapsed_time >= GC.EGG_HATCH + GC.BABY_FIRST_POOP and not last_poo > GC.BABY_FIRST_POOP:
                poo += 1
                last_poo = elapsed_time
            elif elapsed_time >= random.choice([GC.BABY_SECOND_POOP_HIGHER, GC.BABY_SECOND_POOP_LOWER]) and not last_poo >= GC.BABY_SECOND_POOP_HIGHER:
                poo += 1
                last_poo = GC.BABY_SECOND_POOP_HIGHER
            if elapsed_time >= GC.BABY_SPAN:
                age = 2
                prev_age = 1

        # handle Aging
        if stage != "baby":
            day_time = datetime.datetime.now().hour
            if day_time >= sleep_start or day_time < sleep_end:
                if not asleep: asleep = True
                if wants_timeouts["sleepy"] == -2:
                    create_wants("sleepy")
            elif sleep_start > day_time >= sleep_end:
                if wants_timeouts["sleepy"] == -1 and prev_age + 1 == age:
                    prev_age = age
                    age += 1
                    wants_timeouts["sleepy"] = -2

        # handle if stage change required
        if  GC.TEEN_AGE > age >= GC.CHILD_AGE:
            stage = "child"
        elif GC.ADULT_AGE > age >= GC.TEEN_AGE:
            stage = "teen"
        elif GC.SPEC_ADULT_AGE > age >= GC.ADULT_AGE:
            stage = "adult"
        elif age >= GC.SPEC_ADULT_AGE and stage != "adult_spec":
            stage = "adult_spec"
        elif age >= GC.OLD_AGE_DEATH:
            stage = "dead"

        # handle child specific event
        if stage == "child":
            if elapsed_time >= GC.CHILD_FIRST_POOP:
                poo += 1
                last_poo = GC.CHILD_FIRST_POOP

        # handle stage events
        # poo event
        if elapsed_time >= last_poo + GC.FINAL_POOP_INTERVAL:
            poo += 1
            last_poo = elapsed_time
        # hunger loss event
        if elapsed_time >= last_hunger + GC.MAX_HUNGER_LOSS_RATE:
            hunger = max(0, hunger - 1)
            last_hunger = elapsed_time
        # happy loss event
        if elapsed_time >= last_happy + GC.MAX_HAPPY_LOSS_RATE:
            happy = max(0, happy - 1)
            last_happy = elapsed_time
        # happy or hunger death event
        if (elapsed_time >= last_happy + 2 * GC.MAX_HAPPY_LOSS_RATE and happy == 0) or (elapsed_time >= last_hunger + 2 * GC.MAX_HUNGER_LOSS_RATE and hunger == 0):
            stage = "dead"
        # poo sickness event
        if poo > 1  and elapsed_time >= last_poo + round(GC.ATTENTION_TIMEOUT / 2):
            create_wants("sick")
        # discipline event
        if elapsed_time >= last_happy + GC.ATTENTION_TIMEOUT:
            if random.randint(0,1) and random.randint(discipline,4) < 4:
                create_wants("fake")

    elif stage == "egg": # handle time updates for egg stage
        if elapsed_time >= GC.EGG_HATCH:
            stage = "baby"
            last_poo = elapsed_time
            age = 1

# game loop
while run:
    clock.tick(GC.FPS)

    # poll for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # handle saving game here
            save_game()
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for btn_name, btn_location in btn_locations.items():
                if (btn_name in active_btns) and btn_location.collidepoint(event.pos):
                    print(f"{btn_name} pressed")
                    btn_event_handler(btn_name)
                    last_click = time.monotonic()

    # render game here
    # set if light on or off
    if light:
        display.fill("white")
    else:
        display.fill("black")
    # set displayed btns
    for btn_name, btn_location in btn_locations.items():
        if btn_name in active_btns:
            display.blit(btn_images[btn_name], btn_location.topleft)
    # set tamagotchi display (or stat display)
    if light:
        stat_imgs = []
        if current_display == 0:
            display.blit(stage_images[stage], GC.TAMA_POSITION)
        elif current_display == 1:
            for i in range(happy):
                stat_imgs.append(stat_images["heart_filled"])
            for i in range(4 - happy):
                stat_imgs.append(stat_images["heart_empty"])
            for i, img in enumerate(stat_imgs):
                display.blit(img, (GC.STAT_ROW_POSITION[0] + i * GC.STAT_SIZE, GC.STAT_ROW_POSITION[1]))
            display.blit(GAME_FONT.render("HAPPY", 1, (0, 0 ,0)), (GC.STAT_ROW_POSITION[0], GC.STAT_ROW_POSITION[1] - GC.STAT_SIZE - 10))
        elif current_display == 2:
            for i in range(hunger):
                stat_imgs.append(stat_images["heart_filled"])
            for i in range(4 - hunger):
                stat_imgs.append(stat_images["heart_empty"])
            for i, img in enumerate(stat_imgs):
                display.blit(img, (GC.STAT_ROW_POSITION[0] + i * GC.STAT_SIZE, GC.STAT_ROW_POSITION[1]))
            display.blit(GAME_FONT.render("HUNGER", 1, (0, 0, 0)),
                         (GC.STAT_ROW_POSITION[0], GC.STAT_ROW_POSITION[1] - GC.STAT_SIZE - 10))
        elif current_display == 3:
            for i in range(discipline):
                stat_imgs.append(stat_images["discipline_filled"])
            for i in range(4 - discipline):
                stat_imgs.append(stat_images["discipline_empty"])
            for i, img in enumerate(stat_imgs):
                display.blit(img, (GC.STAT_ROW_POSITION[0] + i * GC.STAT_SIZE, GC.STAT_ROW_POSITION[1]))
            display.blit(GAME_FONT.render("DISCIPLINE", 1, (0, 0, 0)),
                         (GC.STAT_ROW_POSITION[0], GC.STAT_ROW_POSITION[1] - GC.STAT_SIZE - 10))
        elif current_display == 4:
            display.blit(GAME_FONT.render(f"AGE: {age} years", 1, (0, 0, 0)),
                         (GC.STAT_ROW_POSITION[0], GC.STAT_ROW_POSITION[1]))
        elif current_display == 5:
            display.blit(GAME_FONT.render(f"WEIGHT: {weight} lbs", 1, (0, 0, 0)),
                         (GC.STAT_ROW_POSITION[0], GC.STAT_ROW_POSITION[1]))

    # update game display
    pygame.display.update()

    # handle game updates by time
    handle_timed_events()

# close program
pygame.quit()