# file paths
SAVE_FILE = 'game_save/save_data.json'
BTN_PATH = 'assets/btn_images/'
BTN_NAMES = ['attention_not_wanted', 'attention_wanted', 'bathroom', 'discipline',
             'food', 'game', 'light_off', 'light_on', 'medicine', 'meter']
STAGE_PATH = 'assets/tamagotchi_stages/'
STAGE_TEEN_PATH = 'teenagers/teenager_'
STAGE_ADULT_PATH = 'adults/adult_'
STAGE_SPEC_ADULT_PATH = 'adults_special/adult_special_'

# define a minute in seconds
MIN_S = 60

# egg hatching time of tamagotchi
EGG_HATCH = 5 * MIN_S
# baby time span from egg hatch to child age
BABY_SPAN = 65 * MIN_S
# age at which tamagotchi becomes child, teen, adult, or special adult
CHILD_AGE = 2
TEEN_AGE = 13
ADULT_AGE = 21
SPEC_ADULT_AGE = 45

# attention timeout
ATTENTION_TIMEOUT = 15 * MIN_S

# max heart loss rates
MAX_HUNGER_LOSS_RATE = 6 * MIN_S
MAX_HAPPY_LOSS_RATE = 7 * MIN_S

# poop intervals
# baby stage intervals
BABY_FIRST_POOP = 15 * MIN_S
BABY_SECOND_POOP_LOWER = 40 * MIN_S
BABY_SECOND_POOP_HIGHER = 45 * MIN_S
CHILD_FIRST_POOP = 5 * MIN_S
FINAL_POOP_INTERVAL = 3 * 60 * MIN_S

# lower and upper bounds of higher lower game
GAME_LOW = 1
GAME_HIGH = 9