from vpython import *
import numpy as np
from bodies import Bodies, DT
from node import *
from numba import jit
import copy as cp

SEED = "monoszijnsuf"
STARTSIZE = 1.5E14
STARTSPEED =  110E6
RANDOM = True
TREECODE = False
np.random.seed(sum(ord(char) for char in SEED))

N = 100
DT = 1000
G = 6.67E-11


def randombodies(num):
    randarr = STARTSIZE*np.random.rand(num,2)
    theta= 2*np.pi*np.random.rand(num,1)
    pos = np.array([(STARTSIZE*rand[0]*np.cos(2*np.pi*rand[1]), STARTSIZE*rand[0]*np.sin(2*np.pi*rand[1]),0) for rand in randarr])
    vel = np.random.rand(num,3)
    return Bodies(pos, vel)


def main():
    
    universe = randombodies(N)
    print('generated random bodies')

    planet = []
    TIME = 0
    oldnum = universe.num
    
    for i in range(0, universe.num):
        planet.append(sphere(pos=vector(*(universe.pos[i][:])), radius = universe.radius[i], color=color.white))

    while True:
        universe.do3Sim()
        TIME += DT
        test = universe.num < oldnum

        print(TIME)
        for i in range(0, universe.num):
            planet[i].pos = vector(*(universe.pos[i][:]))
            if test:
                planet[i].radius = (universe.radius[i])
        
        if test:
            for j in range(0, oldnum - universe.num):
                planet[j + universe.num].visible = False
        
        oldnum = cp.deepcopy(universe.num)
    

if __name__ == "__main__":
    main()
