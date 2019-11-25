# -*- coding: utf-8 -*-
"""
Created on Mon Nov 18 17:10:29 2019

@author: Julian
"""

import numpy as np
from Star import Body
from universe import Universe


#Parameters:

RADIUS = 695510e-9  # Pm (=10^12 m)
RHO = 1.41e3        # Lg/Pm^3 
M = 1.989           # Lg (=10^30 kg)
DIST = 5e13
DT = 
VEL = 5e3
SEED = "monoszijnsuf"
np.random.seed(sum(ord(char) for char in SEED))

def main():
    """
    N = 2
    bodies = []
    randomvals = 1e12*np.random.rand(N,6)          
    for vals in randomvals:
        mass = 1.989e30
        color = np.random.rand(3)
        bodies += [Body( (vals[0],vals[1],0), (1e3,0,0), mass = mass, color = color)]
    """
    a = Body((DIST,0,0), (0,5e3,0), mass = M, color = (0.8,0.8,1))
    b = Body((-DIST,0,0), (0,-5e3,0), mass = M, color = (1,0.8,0.8))
    bodies = [a,b]
    universe = Universe(bodies, G=1e-29)
    #universe.draw()
    #print(universe.bodyList)
    while True:
        #(universe.bodyList)
        universe.update()
        #print(universe.bodyList)
   
if __name__ == "__main__":
    main()