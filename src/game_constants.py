# display constants
WIDTH, HEIGHT = 1280, 720
# scale factors for images (based on 1280 by 720)
BTN_SCALE_FACTOR = 75 / 1280
STAT_SCALE_FACTOR = 80 / 1280
TAMA_SCALE_FACTOR = 200 / 1280
BTN_SIZE = max(1, int(WIDTH * BTN_SCALE_FACTOR))
STAT_SIZE = max(1, int(WIDTH * STAT_SCALE_FACTOR))
TAMA_SIZE = max(1, int(WIDTH * TAMA_SCALE_FACTOR))

# btn constants
BTNS_PER_ROW = 4
BTN_GAP = (BTN_SIZE // 2)
BTN_ROW_TOP = ((WIDTH // (BTNS_PER_ROW + 1)), 10)
BTN_ROW_BOTTOM = ((WIDTH // (BTNS_PER_ROW + 1)), HEIGHT - BTN_SIZE - 10)

# file paths
SAVE_FILE = 'game_save/save_data.json'
# btn image paths
BTN_PATH = 'assets/btn_images/'
BTN_NAMES = ['attention_not_wanted', 'attention_wanted', 'bathroom', 'discipline',
             'food', 'game', 'light_off', 'light_on', 'medicine', 'meter']
# stage image paths
STAGE_PATH = 'assets/tamagotchi_stages/'
STAGE_TEEN_PATH = 'teenagers/teenager_'
STAGE_ADULT_PATH = 'adults/adult_'
STAGE_SPEC_ADULT_PATH = 'adults_special/adult_special_'
# stat image paths
STAT_PATH = 'assets/stat_images/'
STAT_NAMES = ['discipline_empty', 'discipline_filled', 'heart_empty', 'heart_filled']

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