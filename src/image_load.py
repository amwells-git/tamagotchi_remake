# get common imports
from src.common_imports import *

# functions for loading required images
def get_btn_images():
    btn_images = {}
    for image in gc.BTN_NAMES:
        btn_images[image] = pygame.transform.scale(pygame.image.load(gc.BTN_PATH + image + '.png'), (gc.BTN_SIZE, gc.BTN_SIZE))
    return btn_images

def get_stage_images(teen_ver, adult_ver):
    stage_images = {}
    stage_images["egg"] = pygame.image.load(gc.STAGE_PATH + 'egg.png')
    stage_images["baby"] = pygame.image.load(gc.STAGE_PATH + 'baby.png')
    stage_images["child"] = pygame.image.load(gc.STAGE_PATH + 'child.png')
    stage_images["dead"] = pygame.image.load(gc.STAGE_PATH + 'dead.png')
    stage_images["teen"] = pygame.image.load(gc.STAGE_PATH + gc.STAGE_TEEN_PATH + str(teen_ver) + '.png')
    stage_images["adult"] = pygame.image.load(gc.STAGE_PATH + gc.STAGE_ADULT_PATH + str(adult_ver) + '.png')
    stage_images["adult_spec"] = pygame.image.load(gc.STAGE_PATH + gc.STAGE_SPEC_ADULT_PATH + str(adult_ver) + '.png')

    for img_name, img in stage_images.items():
        stage_images[img_name] = pygame.transform.scale(img, (gc.TAMA_SIZE, gc.TAMA_SIZE))

    return stage_images

def get_stat_images():
    stat_images = {}
    for image in gc.STAT_NAMES:
        stat_images[image] = pygame.transform.scale(pygame.image.load(gc.STAT_PATH + image + '.png'), (gc.STAT_SIZE, gc.STAT_SIZE))
    return stat_images

def get_condition_images():
    condition_images = {}
    for image in gc.CONDITION_NAMES:
        condition_images[image] = pygame.transform.scale(pygame.image.load(gc.CONDITION_PATH + image + '.png'),
                                                         (gc.CONDITION_SIZE, gc.CONDITION_SIZE))
    return condition_images