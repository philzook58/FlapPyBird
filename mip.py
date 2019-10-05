import cvxpy as cvx
import numpy as np
import matplotlib.pyplot as plt

N = 50 # time steps
dt = 0.1
path = cvx.Variable((N, 3)) # x/y pos and vel
f = cvx.Variable(N-1, boolean=True) # force
vx = 1
g = 9.8
j = 10 # impulse factor
recovery = 10

# unpack variables
x = path[:,0]
y = path[:,1]

vy = path[:,2]

c = [] #constraints
c += [f >= 0] # only fire rocket downward
c += [x[0] == 0, vx[0] == 0, y[0] == 10, vy[0] == 0]

for t in range(N-1):
    c += [x[t + 1] ==  x[t] + vx*dt ]
    c += [y[t + 1] ==  y[t] + vy[t]*dt ]
    c += [vy[t + 1] ==  vy[t] - g * dt + j * f[t] ]
for t in range(N-recovery):
    c += [cvx.sum(f[t:t+recovery] <= 1] # not more than one impulse in recovery window. Is there a recovery window?

c += [y[N-1] == 0] # landed
c += [vy[N-1] == 0] # gently vx[N-1] == 0


# keep position inside allowable region.

objective = cvx.Minimize(cvx.sum(f)) # minimize total fuel use

prob = cvx.Problem(objective, c)
prob.solve(verbose = True)
plt.plot(y.value, label="height")
plt.plot(f.value, label="force")
plt.legend()
plt.title("Height vs Time")
plt.show()

