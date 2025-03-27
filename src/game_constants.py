# get common imports
from src.common_imports import *

# display constants
WIDTH, HEIGHT = 1280, 720
FPS = 60
# font constants
FONT_STYLE = "comicsans"
FONT_SCALE_FACTOR = 60 / 1280
FONT_SIZE = max(1, int(WIDTH * FONT_SCALE_FACTOR))
# scale factors for images (based on 1280 by 720)
BTN_SCALE_FACTOR = 75 / 1280
STAT_SCALE_FACTOR = 80 / 1280
TAMA_SCALE_FACTOR = 200 / 1280
CONDITION_SCALE_FACTOR = 65 / 1280
BTN_SIZE = max(1, int(WIDTH * BTN_SCALE_FACTOR))
STAT_SIZE = max(1, int(WIDTH * STAT_SCALE_FACTOR))
STAT_ROW_POSITION = ((WIDTH - (STAT_SIZE * 4)) // 2, (HEIGHT - STAT_SIZE) // 2)
TAMA_SIZE = max(1, int(WIDTH * TAMA_SCALE_FACTOR))
TAMA_POSITION = (((WIDTH - TAMA_SIZE) // 2), ((HEIGHT - TAMA_SIZE) // 2))
CONDITION_SIZE = max(1, int(WIDTH * CONDITION_SCALE_FACTOR))

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
# condition image paths
CONDITION_PATH = 'assets/condition_images/'
CONDITION_NAMES = ['poo', 'sick']

# define a minute in seconds
MIN_S = 60

# egg hatching time of tamagotchi
EGG_HATCH = 10 #TODO: Make 5 * MIN_S
# baby time span from egg hatch to child age
BABY_SPAN = 20 #TODO: Make 65 * MIN_S + EGG_HATCH
# age at which tamagotchi becomes child, teen, adult, or special adult
CHILD_AGE = 2
TEEN_AGE = 13
ADULT_AGE = 21
SPEC_ADULT_AGE = 45
OLD_AGE_DEATH = 80

# attention timeout
ATTENTION_TIMEOUT = MIN_S #TODO: MAKE 15 * MIN_S

# max heart loss rates
MAX_HUNGER_LOSS_RATE = 1 * MIN_S #TODO: MAKE 6 * MIN_S
MAX_HAPPY_LOSS_RATE = 2 * MIN_S #TODO: MAKE 7 * MIN_S

# poop intervals
# baby stage intervals
BABY_FIRST_POOP = 2 * MIN_S #TODO: MAKE 15 * MIN_S
BABY_SECOND_POOP_LOWER = 3 * MIN_S #TODO: MAKE 40 * MIN_S
BABY_SECOND_POOP_HIGHER = 4 * MIN_S #TODO: MAKE 45 * MIN_S
CHILD_FIRST_POOP = 50 * MIN_S
FINAL_POOP_INTERVAL = 3 * 60 * MIN_S

# weight limit for determining if to make sick
WEIGHT_SICK_LIMIT = 50

# lower and upper bounds of higher lower game
GAME_LOW = 1
GAME_HIGH = 9

# inital / new game data
GAME_INIT_DATA = {
    "age": 0,  # int
    "stage": "egg",  # str from ["egg", "baby", "child", "teen", "adult", "adult_spec", "dead"]
    "start_time": 0,  # rounded time.monotonic()
    "elapsed_time": 0,  # long
    "save_time": time.time(),  # time.time()
    "hunger": 4,  # int [0,4]
    "last_hunger": 0,  # long
    "happy": 4,  # int [0,4]
    "last_happy": 0,  # long
    "discipline": 0,  # int [0,4]
    "weight": 1,  # int [1,]
    "poo": 0,  # int [0,] number of poo on screen
    "last_poo": 0,  # long of last time poo was increased
    "sick": 0,  # int [0,2] sickness level
    "teen_ver": 1,  # TODO: will be randomly set between [1,2] for new games
    "adult_ver": 1,  # TODO: will be randomly set between [1,6] for new games
    "current_wants": [],
    # [str,] each string is a specific want from ['hungry', 'unhappy', 'sick', 'sleepy', 'fake']
    "asleep": False,  # if asleep, used for 'sleepy' want
    "sleep_start": 20,  # TODO: will be randomly set between [18,23] for new games
    "sleep_end": 6,  # TODO: will be randomly set between [0,8] for new games
    "light": True,  # if light is on or off
    # if -1, that means timeout isn't active
    # if 'sleep' is -1, allows age to be increased (-2 means isn't active and can be active)
    "wants_timeouts": {'hungry': -1, 'unhappy': -1, 'sick': -1, 'sleepy': -2, 'fake': -1}
}