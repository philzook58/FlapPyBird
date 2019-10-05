import cvxpy as cvx
import numpy as np
import matplotlib.pyplot as plt

def solve(playery, playerVelY, lowerPipes):
    print(playerVelY)
    PIPEGAPSIZE  = 100
    PIPEWIDTH = 52
    BIRDWIDTH = 34
    BIRDHEIGHT = 24
    BIRDDIAMETER = np.sqrt(BIRDHEIGHT**2 + BIRDWIDTH**2)
    SKY = 0
    GROUND = (512*0.79)-1
    PLAYERX = 57

    pipeVelX = -4

    # player velocity, max velocity, downward accleration, accleration on flap
    #playerVelY    =  -9   # player's velocity along Y, default same as playerFlapped
    playerAccY    =   1   # players downward accleration
    playerFlapAcc =  -14   # players speed on flapping

    N = 30 # time steps to look ahead
    dt = 1.
    path = cvx.Variable((N, 2)) # y pos and vel
    flap = cvx.Variable(N-1, boolean=True) # whether or not the bird should flap in each step

    def getPipeConstraints(x, y, lowerPipes):
        constraints = []
        for pipe in lowerPipes:
            dist_from_front = pipe['x'] - x - BIRDDIAMETER
            dist_from_back = pipe['x'] - x + PIPEWIDTH
            if (dist_from_front < 0) and (dist_from_back > 0):
                print(pipe['y'] + BIRDDIAMETER,  pipe['y'] + PIPEGAPSIZE)
                constraints += [y <= (pipe['y'] - BIRDDIAMETER)] # y above lower pipe
                constraints += [y >= (pipe['y'] - PIPEGAPSIZE)] # y below upper pipe
        if len(constraints) > 0:
            print(constraints)
        return constraints
        

    # unpack variables
    y = path[:,0]

    vy = path[:,1]

    c = [] #constraints
    c += [y <= GROUND, y >= SKY]
    c += [y[0] == playery, vy[0] == playerVelY]

    x = PLAYERX
    xs = [x]
    for t in range(N-1):
        x -= pipeVelX
        xs += [x]
        c += [y[t + 1] ==  y[t] + vy[t]*dt ]
        c += [vy[t + 1] ==  vy[t] + playerAccY * dt + playerFlapAcc * flap[t] ]
        c += getPipeConstraints(x, y[t+1], lowerPipes)


    #objective = cvx.Minimize(cvx.sum(flap)) # minimize total fuel use
    objective = cvx.Minimize(cvx.sum(flap) + 10* cvx.sum(cvx.abs(vy))) # minimize total fuel use

    prob = cvx.Problem(objective, c)
    prob.solve(verbose = False)
    #print(np.round(flap.value).astype(bool))
    #plt.plot(y.value)
    #plt.show()
    return np.round(flap.value).astype(bool)[0], list(zip(xs, y.value))


