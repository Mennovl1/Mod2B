from vpython import *
import numpy as np
from bodiesJulian import Bodies, DT
from node import *
from numba import jit
import copy as cp

SEED = "monoszijnsuf"
TREECODE = False
np.random.seed(sum(ord(char) for char in SEED))

N = 500
G = 6.67
STARTSIZE = 5e5 #in Gamma meter


def randombodies(num):
    randarr = np.random.rand(num,2)
    pos = np.array([(STARTSIZE*rand[0]*np.cos(2*np.pi*rand[1]), STARTSIZE*rand[0]*np.sin(2*np.pi*rand[1]),0) for rand in randarr])
    vel = np.zeros((num,3))#np.random.rand(num,3)
    print(randarr)
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
        #print(TIME)
        print(planet[0].pos)
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
