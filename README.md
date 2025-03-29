# Tamagotchi™ Remade
This project is an attempt to develop a program using Pygame that replicates the original Tamagotchi™ devices.

### _**Warning**_
This project is still a work in progress, as such it does not have all the expected functionality of the original device, nor does it have all required images.

## Packages
This project is developed entirely with the Pygame package in Python.

## Running the Game
To run this project, download & extract the main branch to a directory in your system.

Then, run your Python compiler from the extracted folder containing main.py using
>python main.py

### Game interactions
To interact with the game you can click on the images on the top and bottom of the screen.
Each of the images does what the original device interaction intended. For example, The top left button will feed or provide snacks to the creature.

#### The Meter
Changes the central display to show statistics about the creature. Will move through Happy, Hunger, Discipline, Age, Weight, and then back to the creature in that order.

### The Creature's Life Span
To keep it simple, the creature's life span is only calculated using the time the program is running, and as such by closing the program it is held in an effective 'stasis' until the program is run again.

## Future Work
- Add sickness and bathroom functionality to project.
- Add background image / design to make project look cleaner

## _Using Project In Current State_
If you wish to use the unfinished project as it currently is, you will need to add a few directories:
1. One directory on the same level as `src` & `assets` named `game_save`
2. Two directories on the same level as `btn_images` & `stat_images` named `tamagotchi_stages` & `condition_images` respectively
3. Three directories within `tamagotchi_stages` named `adults`, `adults_special`, & `teenagers` respectively

Then you will need to add a few images in the `.png` format to some directories:
1. In `tamagotchi_stages` you will need to add:
    1. `baby.png`
    2. `child.png`
    3. `dead.png`
    4. `egg.png`
    5. In `adults` add `adult_1.png`
    6. In `adults_special` add `adult_special_1.png`
    7. In `teenagers` add `teenager_1.png`
2. In `condition_images` you will need to add:
    1. `poo.png`
    2. `sick.png`

The `condition_images` are required even though the functionality is not yet implemented as they are loaded by the program when it is run.

## Tamagotchi™ Copyright Notice
Tamagotchi™ and all related images, icons, and trademarks are © Bandai. 
All rights reserved. This project is fan work and is not affiliated with or endorsed by Bandai.
