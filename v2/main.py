from vpython import *
import numpy as np
from bodies import Bodies
from node import *
from numba import jit

SEED = "monoszijnsuf"
STARTSIZE = 1.5E14
STARTSPEED =  110E6
RANDOM = True
TREECODE = True
np.random.seed(sum(ord(char) for char in SEED))


def randombodies(num):
    pos = 2 * STARTSIZE * (np.random.rand(num, 3) - 0.5)
    vel = 2 * STARTSPEED * (np.random.rand(num, 3) - 0.5)
    return Bodies(pos, vel)


def main():
    
    if RANDOM:
        universe = randombodies(5000)
        print('generated random bodies')
    else:
        pos = np.array([[1, 1, 1], [-1, 1, 1], [1, 2, -1]])
        vel = np.zeros((3, 3))
        universe = Bodies(pos, vel)

    print("Building tree \n")
    root = buildTree(universe, STARTSIZE * 2)
    print('Done \n')
    # print(root)
    
    # planet = []
    # TIME = 0
    # oldnum = universe.num

    '''
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
    '''

if __name__ == "__main__":
    main()