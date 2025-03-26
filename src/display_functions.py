import pygame
from src import game_constants as GC

def get_btn_images():
    btn_images = {}
    for image in GC.BTN_NAMES:
        btn_images[image] = pygame.image.load(GC.BTN_PATH + image + '.png')
    return btn_images

def get_stage_images(teen_ver, adult_ver):
    stage_images = {}
    stage_images["egg"] = pygame.image.load(GC.STAGE_PATH + 'egg.png')
    stage_images["baby"] = pygame.image.load(GC.STAGE_PATH + 'baby.png')
    stage_images["child"] = pygame.image.load(GC.STAGE_PATH + 'child.png')
    stage_images["teen"] = pygame.image.load(GC.STAGE_PATH + GC.STAGE_TEEN_PATH + str(teen_ver) + '.png')
    stage_images["adult"] = pygame.image.load(GC.STAGE_PATH + GC.STAGE_ADULT_PATH + str(adult_ver) + '.png')
    stage_images["adult_spec"] = pygame.image.load(GC.STAGE_PATH + GC.STAGE_SPEC_ADULT_PATH + str(adult_ver) + '.png')
    return stage_images