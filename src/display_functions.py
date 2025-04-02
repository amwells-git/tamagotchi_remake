# get common imports
from src.common_imports import *

# `dis` is pygame display from main.py

# define display filling function
def fill_display(dis, light):
    if light: dis.fill('white')
    else: dis.fill('black')

# button displaying function
def display_btns(dis, active_btns, btn_images, btn_locations):
    for btn_name, btn_location in btn_locations.items():
        if btn_name in active_btns:
            dis.blit(btn_images[btn_name], btn_location.topleft)

# stat image display helper func
def display_stat_img(dis, game_data, stat_images, FONT, stat):
    # decide which image pair is to be used
    if stat == 'happy' or stat == 'hunger':
        img = 'heart_'
    else: img = 'discipline_'

    # list of images to be displayed
    stat_imgs = []

    # get number of filled images
    for i in range(game_data[stat]):
        stat_imgs.append(stat_images[img + 'filled'])
    # get remaining number of empty images
    for i in range(4 - game_data[stat]):
        stat_imgs.append(stat_images[img + 'empty'])

    # display stat_imgs
    for i, image in enumerate(stat_imgs):
        dis.blit(image, (gc.STAT_ROW_POSITION[0] + i * gc.STAT_SIZE, gc.STAT_ROW_POSITION[1]))

    # display stat name
    dis.blit(FONT.render(stat.upper(), 1, (0, 0, 0)),
                 (gc.STAT_ROW_POSITION[0], gc.STAT_ROW_POSITION[1] - gc.STAT_SIZE - 10))

# tamagotchi / stat display function
def display_tama(dis, game_data, current_display, stage_images, stat_images, FONT):
    # this is only shown when light is "on"
    if game_data['light']:
        if current_display == 0: # show tamagotchi
            dis.blit(stage_images[game_data['stage']], gc.TAMA_POSITION)
        elif current_display == 1: # show happy stat
            display_stat_img(dis, game_data, stat_images, FONT, 'happy')
        elif current_display == 2: # show hunger stat
            display_stat_img(dis, game_data, stat_images, FONT, 'hunger')
        elif current_display == 3: # show discipline stat
            display_stat_img(dis, game_data, stat_images, FONT, 'discipline')
        elif current_display == 4: # show age
            dis.blit(FONT.render(f"AGE: {game_data['age']} years", 1, (0, 0, 0)),
                         (gc.STAT_ROW_POSITION[0], gc.STAT_ROW_POSITION[1]))
        elif current_display == 5: # show weight
            dis.blit(FONT.render(f"WEIGHT: {game_data['weight']} lbs", 1, (0, 0, 0)),
                         (gc.STAT_ROW_POSITION[0], gc.STAT_ROW_POSITION[1]))

# display sickness icon
def display_sick(dis, game_data, condition_images, position):
    if game_data['light'] and game_data['sick'] > 0:
        dis.blit(condition_images['sick'], (position[0], position[1] + gc.BTN_SIZE + 10))

# display poo
def display_poo(dis, game_data, condition_images, poo_locations):
    # if poo is greater than poo_locations size, add poo
    if game_data['poo'] > len(poo_locations):
        while len(poo_locations) < game_data['poo']:
            # generate a random x, y location for poo
            poo_x = random.randint(gc.POO_TOP_LEFT_LIMIT[0], gc.POO_BOTTOM_RIGHT_LIMIT[0])
            poo_y = random.randint(gc.POO_TOP_LEFT_LIMIT[1], gc.POO_BOTTOM_RIGHT_LIMIT[1])
            # only use if within poo window limit
            if (poo_x + gc.CONDITION_SIZE) <= gc.POO_BOTTOM_RIGHT_LIMIT[0] and (poo_y + gc.CONDITION_SIZE) <= gc.POO_BOTTOM_RIGHT_LIMIT[1]:
                poo_locations.append((poo_x, poo_y))
    # if poo is less tan poo_locations size, remove poo locations randomly or entirely
    if game_data['poo'] == 0:
        poo_locations.clear()
    elif game_data['poo'] < len(poo_locations):
        while len(poo_locations) > game_data['poo']:
            poo_locations.pop(random.randint(0, len(poo_locations) - 1))
    # display poo
    for poo_location in poo_locations:
        dis.blit(condition_images['poo'], poo_location)

    # return updated poo_locations
    return poo_locations