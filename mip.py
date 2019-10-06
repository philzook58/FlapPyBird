import cvxpy as cvx
import numpy as np
import matplotlib.pyplot as plt


N = 20 # time steps to look ahead
path = cvx.Variable((N, 2)) # y pos and vel
flap = cvx.Variable(N-1, boolean=True) # whether or not the bird should flap in each step
last_solution = [False, False, False]
last_path = [(0,0),(0,0)]

PIPEGAPSIZE  = 100
PIPEWIDTH = 52
BIRDWIDTH = 34
BIRDHEIGHT = 24
BIRDDIAMETER = np.sqrt(BIRDHEIGHT**2 + BIRDWIDTH**2)
SKY = 0
GROUND = (512*0.79)-1
PLAYERX = 57


def getPipeConstraints(x, y, lowerPipes):
    constraints = []
    for pipe in lowerPipes:
        dist_from_front = pipe['x'] - x - BIRDDIAMETER
        dist_from_back = pipe['x'] - x + PIPEWIDTH
        if (dist_from_front < 0) and (dist_from_back > 0):
            #print(pipe['y'] + BIRDDIAMETER,  pipe['y'] + PIPEGAPSIZE)
            constraints += [y <= (pipe['y'] - BIRDDIAMETER)] # y above lower pipe
            constraints += [y >= (pipe['y'] - PIPEGAPSIZE)] # y below upper pipe
    #if len(constraints) > 0:
        #print(constraints)
    return constraints

def solve(playery, playerVelY, lowerPipes):
    global last_path, last_solution

    print(last_path)
    pipeVelX = -4
    playerAccY    =   1   # players downward accleration
    playerFlapAcc =  -14   # players speed on flapping

    # unpack variables
    y = path[:,0]

    vy = path[:,1]

    c = [] #constraints
    c += [y <= GROUND, y >= SKY]
    c += [y[0] == playery, vy[0] == playerVelY]

    x = PLAYERX
    xs = [x]
    for t in range(N-1):
        dt = t//10 + 1
        #dt = 1
        x -= dt * pipeVelX
        xs += [x]
        c += [vy[t + 1] ==  vy[t] + playerAccY * dt + playerFlapAcc * flap[t] ]
        c += [y[t + 1] ==  y[t] + vy[t + 1]*dt ]
        c += getPipeConstraints(x, y[t+1], lowerPipes)


    #objective = cvx.Minimize(cvx.sum(flap)) # minimize total fuel use
    objective = cvx.Minimize(cvx.sum(flap) + 10* cvx.sum(cvx.abs(vy))) # minimize total fuel use

    prob = cvx.Problem(objective, c)
    try:
        prob.solve(verbose = False, solver="GUROBI")
        #print(np.round(flap.value).astype(bool))
        #plt.plot(y.value)
        #plt.show()
        last_path = list(zip(xs, y.value))
        last_solution = np.round(flap.value).astype(bool)
        return last_solution[0], last_path
    except:
        last_solution = last_solution[1:]
        last_path = [((x-4), y) for (x,y) in last_path[1:]]
        return last_solution[0], last_path


