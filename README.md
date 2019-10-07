FlapPyBird-MPC
===============

![A happy flappy boy](flappy_bird.gif)

A Mixed Integer Programming model predictive controller for a [Flappy Bird Clone](https://github.com/sourabhv/FlapPyBird). The meat of the controller is found in `mip.py`. Most of the rest is unmodified from the original flappy bird clone.

Blog posts describing the approach can be found here:

- http://www.philipzucker.com/flappy-bird-as-a-mixed-integer-program/
- http://blog.benwiener.com/programming/2019/10/06/flappy-bird-mpc.html

How-to (as tested on MacOS)
---------------------------

1. Install pygame, cvxpy, gurobi, numpy. 
2. `python flappy.py` hit space and watch her go.
