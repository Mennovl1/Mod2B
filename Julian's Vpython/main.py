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
RHO = 1.41e9        # Lg/Pm^3 
M = 1.989           # Lg (=10^30 kg)
DIST = 1            # Pm (=10^12 m)
DT = 0.1            # Ms (=10^6 m)
VEL = 5e-3          # Pm/Ms
G = 6.67e-5         # Pm^3/(Lg*Ms^2)
SEED = "monoszijnsuf"
np.random.seed(sum(ord(char) for char in SEED))

def main():
    a = Body((DIST,0,0), (0,VEL,0), mass = M, color = (0.8,0.8,1))
    b = Body((-DIST,0,0), (0,-VEL,0), mass = M, color = (1,0.8,0.8))
    bodies = [a,b]
    universe = Universe(bodies, G=G, dt = DT)
    #universe.draw()
    #print(universe.bodyList)
    while True:
        #(universe.bodyList)
        universe.update()
        #print(universe.bodyList)
   
if __name__ == "__main__":
    main()