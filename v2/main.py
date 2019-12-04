from vpython import *
import numpy as np
from bodiesJulian import Bodies, DT
from node import *
from numba import jit
import copy as cp

SEED = "monoszijnsuf"
STARTSIZE = 5e5 #is reeel
STARTSPEED =  110E6
RANDOM = True
TREECODE = True
np.random.seed(sum(ord(char) for char in SEED))
G = 6.67e10
M = 2000
m=5.972 #2e30 is reel
RHO = 1/(4*np.pi/3*(5.51E3)**3)*(10E-2) #is dit niet 1/4piR^2
N=1000

def randombodies(num):
    vel=np.zeros((num,3))
    pos = (np.random.rand(num, 3))
    for i in range(0,num):
        pos[i][-1]=0
        (pos[i][0],pos[i][1])=(pos[i][0]*STARTSIZE*np.cos(2*np.pi*pos[i][1]),pos[i][0]*STARTSIZE*np.sin(2*np.pi*pos[i][1]))
        vel[i][0]=pos[i][1]*np.sqrt(G*m*N/STARTSIZE)/np.sqrt((pos[i][0])**2+(pos[i][1])**2)
        vel[i][1]=-pos[i][0]*np.sqrt(G*m*N/STARTSIZE)/np.sqrt((pos[i][0])**2+(pos[i][1])**2)
    return Bodies(pos, vel)

def randomBodiesWithBlackHole(num):
    vel=np.zeros((num,3))
    pos = (np.random.rand(num, 3))
    for i in range(0,num):
        pos[i][-1]=0
        (pos[i][0],pos[i][1])=(pos[i][0]*STARTSIZE*np.cos(2*np.pi*pos[i][1]),pos[i][0]*STARTSIZE*np.sin(2*np.pi*pos[i][1]))
        vel[i][0]=pos[i][1]*np.sqrt(G*m*N/STARTSIZE+M/np.sqrt(((pos[i][0])**2+(pos[i][1])**2)))/np.sqrt((pos[i][0])**2+(pos[i][1])**2)*1.3
        vel[i][1]=-pos[i][0]*np.sqrt(G*m*N/STARTSIZE+M/np.sqrt(((pos[i][0])**2+(pos[i][1])**2)))/np.sqrt((pos[i][0])**2+(pos[i][1])**2)*1.3
    print(pos.shape)
    print(np.array([[0,0,0]]).shape)
    pos2 = np.concatenate((np.array([[0,0,0]]), pos), axis=0)
    vel2 = np.concatenate((np.array([[0,0,0]]), vel), axis=0)
    mass2 = np.concatenate((M*np.ones((1,1)),m*np.ones((pos.shape[0], 1))), axis=0)
    return Bodies(pos2, vel2, mass = mass2)


def main():
    
    if RANDOM:
        universe = randomBodiesWithBlackHole(N)
        print('generated random bodies')
    else:
        pos = np.array([[1, 1, 1], [-1, 1, 1], [1, 2, -1]])
        vel = np.zeros((3, 3))
        universe = Bodies(pos, vel)

    # print("Building tree \n")
    # root = buildTree(universe, STARTSIZE * 2)
    # print('Done \n')
    # # print(root)
    
    planet = []
    TIME = 0
    oldnum = universe.num

    
    for i in range(0, universe.num):
        planet.append(sphere(pos=vector(*(universe.pos[i][:])), radius = universe.radius[i], color=color.white))
    while True:
        universe.do3Sim()
        TIME += DT
        print(universe.num)
        print(oldnum)
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
    canvas.autoscale(False)
if __name__ == "__main__":
    main()