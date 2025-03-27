# get common imports
from src.common_imports import *

# extra imports
from src.save_game import save_game, create_new_game


# solve tamagotchi wants
def solve_wants(game_data, active_btns, want=None):
    # handle want timeout checks
    if want is None:
        for want in game_data['current_wants']:
            if game_data['elapsed_time'] >= game_data['wants_timeouts'][want] != -1:
                # TODO: Handle Care Mistake
                game_data['wants_timeouts'][want] = -1
                game_data['current_wants'].remove(want)
    else: # handle specific want
        if want in game_data['current_wants']:
            game_data['current_wants'].remove(want)
            game_data['wants_timeouts'][want] = -1
            if want == "sick":
                game_data['sick'] = max(0, game_data['sick'] - 1)
            if want == "fake":
                game_data['discipline'] = min(4, game_data['discipline'] + 1)

    # replace attention btn, only if light is on
    if 'attention_wanted' in active_btns and not game_data['current_wants'] and game_data['light']:
        active_btns.remove('attention_wanted')
        active_btns.add('attention_not_wanted')

    # return updated game_data and active_btns
    return game_data, active_btns

# create tamagotchi wants
def create_wants(game_data, active_btns, want):
    if want not in game_data['current_wants']:
        if want == "sick":
            game_data['sick'] = min(2, game_data['sick'] + 1)
        game_data['current_wants'].append(want)
        game_data['wants_timeouts'][want] = game_data['elapsed_time'] + gc.ATTENTION_TIMEOUT

    if game_data['current_wants'] and 'attention_wanted' not in active_btns and game_data['light']:
        if 'attention_not_wanted' in active_btns:
            active_btns.remove('attention_not_wanted')
        active_btns.add('attention_wanted')

    # return updated game_data and active_btns
    return game_data, active_btns

# change active btns based off light state
def set_active_btns(active_btns, light, wants_bool=False):
    active_btns.clear()
    if light:
        active_btns.add("food")
        active_btns.add("light_off")
        active_btns.add("game")
        active_btns.add("medicine")
        active_btns.add("bathroom")
        active_btns.add("meter")
        active_btns.add("discipline")
        if wants_bool:
            active_btns.add("attention_wanted")
        else:
            active_btns.add("attention_not_wanted")
    else:
        active_btns.add("light_on")
    
    # return new list of active btns
    return active_btns

# button event handler
def btn_event_handler(game_data, active_btns, current_display, btn_name):
    if btn_name == "food":
        if game_data['hunger'] != 4:
            game_data, active_btns = solve_wants(game_data, active_btns, "hungry")
            game_data['hunger'] = 4
        else: # considered a snack
            game_data['happy'] = min(4, game_data['happy'] + 1)
            game_data['weight'] += 2
    elif btn_name == "light_off" or btn_name == "light_on":
        if game_data['light']:
            game_data, active_btns = solve_wants(game_data, active_btns, "sleepy")
            game_data['light'] = False
            # update active buttons
            active_btns = set_active_btns(active_btns, game_data['light'], True if game_data['current_wants'] else False)
        else:
            game_data['light'] = True
            # update active btns
            active_btns = set_active_btns(active_btns, game_data['light'])
    elif btn_name == "game":
        # handle Higher Lower Game
        print("play game")
        game_data, active_btns = solve_wants(game_data, active_btns, "unhappy")
        game_data['happy'] = min(4, game_data['happy'] + 1)
        game_data['weight'] = max(1, game_data['weight'] - 1)
    elif btn_name == "medicine":
        game_data, active_btns = solve_wants(game_data, active_btns, "sick")
    elif btn_name == "bathroom":
        game_data['poo'] = 0
    elif btn_name == "meter":
        if current_display == 5:
            current_display = 0
        else:
            current_display += 1
    elif btn_name == "discipline":
        game_data, active_btns = solve_wants(game_data, active_btns, "fake")
    elif btn_name == "attention_wanted" or btn_name == "attention_not_wanted":
        if game_data['stage'] == 'dead':
            game_data = create_new_game()

    # returns updated game_data, active_btns, and current_display
    return game_data, active_btns, current_display

# timed event handler (handles stage changes, poo, hunger / happy loss)
def timed_event_handler(game_data, active_btns):
    # handle stage time updates
    if game_data['stage'] != "egg" and game_data['stage'] != "dead":
        # handle baby stage specific updates
        if game_data['stage'] == "baby":
            if game_data['elapsed_time'] >= gc.EGG_HATCH + gc.BABY_FIRST_POOP and not game_data['last_poo'] > gc.BABY_FIRST_POOP:
                game_data['poo'] += 1
                game_data['last_poo'] = game_data['elapsed_time']
            elif game_data['elapsed_time'] >= random.choice([gc.BABY_SECOND_POOP_HIGHER,
                                                gc.BABY_SECOND_POOP_LOWER]) and not game_data['last_poo'] >= gc.BABY_SECOND_POOP_HIGHER:
                game_data['poo'] += 1
                game_data['last_poo'] = gc.BABY_SECOND_POOP_HIGHER
            if game_data['elapsed_time'] >= gc.BABY_SPAN:
                game_data['age'] = 2

        # handle Aging
        if game_data['stage'] != "baby":
            day_time = datetime.datetime.now().hour
            if day_time >= game_data['sleep_start'] or day_time < game_data['sleep_end']:
                if not game_data['asleep']: game_data['asleep'] = True
                if game_data['wants_timeouts']["sleepy"] == -2:
                    game_data, active_btns = create_wants(game_data, active_btns, "sleepy")
            elif game_data['sleep_start'] > day_time >= game_data['sleep_end']:
                if game_data['wants_timeouts']["sleepy"] == -1:
                    game_data['age'] += 1
                    game_data['wants_timeouts']["sleepy"] = -2

        # handle if stage change required
        if gc.TEEN_AGE > game_data['age'] >= gc.CHILD_AGE:
            game_data['stage'] = "child"
        elif gc.ADULT_AGE > game_data['age'] >= gc.TEEN_AGE:
            game_data['stage'] = "teen"
        elif gc.SPEC_ADULT_AGE > game_data['age'] >= gc.ADULT_AGE:
            game_data['stage'] = "adult"
        elif game_data['age'] >= gc.SPEC_ADULT_AGE and game_data['stage'] != "adult_spec":
            game_data['stage'] = "adult_spec"
        elif game_data['age'] >= gc.OLD_AGE_DEATH:
            game_data['stage'] = "dead"

        # handle child specific event
        if game_data['stage'] == "child":
            if game_data['elapsed_time'] >= gc.CHILD_FIRST_POOP:
                game_data['poo'] += 1
                game_data['last_poo'] = gc.CHILD_FIRST_POOP

        # handle stage events
        # poo event
        if game_data['elapsed_time'] >= game_data['last_poo'] + gc.FINAL_POOP_INTERVAL:
            game_data['poo'] += 1
            game_data['last_poo'] = game_data['elapsed_time']
        # hunger loss event
        if game_data['elapsed_time'] >= game_data['last_hunger'] + gc.MAX_HUNGER_LOSS_RATE:
            if game_data['hunger'] > 0:
                game_data['hunger'] = max(0, game_data['hunger'] - 1)
                game_data['last_hunger'] = game_data['elapsed_time']
            if game_data['hunger'] <= 1:
                game_data, active_btns = create_wants(game_data, active_btns, "hungry")
        # happy loss event
        if game_data['elapsed_time'] >= game_data['last_happy'] + gc.MAX_HAPPY_LOSS_RATE:
            if game_data['happy'] > 0:
                game_data['happy'] = max(0, game_data['happy'] - 1)
                game_data['last_happy'] = game_data['elapsed_time']
            if game_data['happy'] <= 1:
                game_data, active_btns = create_wants(game_data, active_btns, "unhappy")
        # happy or hunger death event
        if (game_data['elapsed_time'] >= game_data['last_happy'] + 2 * gc.MAX_HAPPY_LOSS_RATE and game_data['happy'] == 0) or (
                game_data['elapsed_time'] >= game_data['last_hunger'] + 2 * gc.MAX_HUNGER_LOSS_RATE and game_data['hunger'] == 0):
            game_data['stage'] = "dead"
        # poo sickness event
        if game_data['poo'] > 1 and game_data['elapsed_time'] >= game_data['last_poo'] + round(gc.ATTENTION_TIMEOUT / 2):
            game_data, active_btns = create_wants(game_data, active_btns, "sick")
        # discipline event
        if game_data['elapsed_time'] >= game_data['last_happy'] + gc.ATTENTION_TIMEOUT:
            if random.randint(0, 1) and random.randint(game_data['discipline'], 5) < 4:
                game_data, active_btns = create_wants(game_data, active_btns, "fake")

    elif game_data['stage'] == "egg":  # handle time updates for egg stage
        if game_data['elapsed_time'] >= gc.EGG_HATCH:
            game_data['stage'] = "baby"
            game_data['last_poo'] = game_data['elapsed_time']
            game_data['age'] = 1

    # returns updated game_data and active btns
    return game_data, active_btns

# handle user / pygame events
def pygame_event_handler(game_data, active_btns, current_display, btn_locations):

    # poll events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # save game
            save_game(game_data)
            # return running false, and other data
            return False, game_data, active_btns, current_display
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for btn_name, btn_location in btn_locations.items():
                if (btn_name in active_btns) and btn_location.collidepoint(event.pos):
                    print(f"{btn_name} pressed") # TODO: remove debug
                    game_data, active_btns, current_display = btn_event_handler(game_data, active_btns,
                                                                                current_display, btn_name)
    # return running true and other data
    return True, game_data, active_btns, current_display