# Monkey Agility
Named after the saying; Monkey see, Monkey do.

This is a system to run obstacle course laps in [online video game], and it consists of two components:

## Monkey See:
A machine vision model to interpret the [online video game]'s environment. The model is from [Detectron2](https://github.com/facebookresearch/detectron2).
It was trained on [this notebook](https://colab.research.google.com/drive/16jcaJoc6bCFAQ96jDe2HwtXj7BMD_-m5) using a manually collected and annotated set of in game screenshots.

This model detects the agility course's obstacle regions and outputs x-y coordinates of said obstacles.

![An example of image segmentation using the machine vision model](agility.gif)

## Monkey do:
This component takes the output of the machine vision model and uses it to know how to interact with the in game environment. This is achieved by moving the mouse pointer and clicking the detected agility obstacles. The goal is to interact with the environment as a human would to avoid being flagged as a bot. This is done by using a collection of recorded human mouse movements combined with additional noise. When needed a mouse path is selected at random, then scaled and rotated. This allows the system to path the mouse to and click on obstacles at any location on the screen, progressing the game.


## Logic Flow:
![](logic_flow.png)



------------
The train and val data sets and the model are not uploaded

Run tests from main with `python -m pytest`
