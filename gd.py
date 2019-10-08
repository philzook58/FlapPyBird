import numpy as np
import matplotlib.pyplot as plt

PIPEGAPSIZE  = 100 # gap between upper and lower pipe
PIPEWIDTH = 52
BIRDWIDTH = 34
BIRDHEIGHT = 24
BIRDDIAMETER = np.sqrt(BIRDHEIGHT**2 + BIRDWIDTH**2) # the bird rotates in the game, so we use it's maximum extent
SKY = 0 # location of sky
GROUND = (512*0.79)-1 # location of ground
PLAYERX = 57 # location of bird


def getPipeConstraints(x, y, lowerPipes):
    constraints = [] # init pipe constraint list
    for pipe in lowerPipes:
        dist_from_front = pipe['x'] - x - BIRDDIAMETER
        dist_from_back = pipe['x'] - x + PIPEWIDTH
        if (dist_from_front < 0) and (dist_from_back > 0):
            constraints += [y <= (pipe['y'] - BIRDDIAMETER)] # y above lower pipe
            constraints += [y >= (pipe['y'] - PIPEGAPSIZE)] # y below upper pipe
    return constraints

def solve(playery, playerVelY, lowerPipes):

    pipeVelX = -4 # speed in x
    playerAccY    =   1   # players downward accleration
    playerFlapAcc =  -20   # players speed on flapping
