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
G = 6.67e10
STARTSIZE = 5e6 #in Gamma meter
MASS = 5.972
m = MASS
M = 100*MASS
RADIUS = 4e4
DT = 1e-1

def sigma(r):
    if r<A:
        return 0*r
    elif r>B:
        return 0*r
    else:
        return 

def randombodiesUnif(num):
    randarr = np.random.rand(num,2)
    pos = np.array([(STARTSIZE*rand[0]*np.cos(2*np.pi*rand[1]), STARTSIZE*rand[0]*np.sin(2*np.pi*rand[1]),0) for rand in randarr])
    VEL = np.sqrt(G*MASS*N/STARTSIZE)
    vel = np.array([(-VEL*np.sin(2*np.pi*rand[1]),VEL*np.cos(2*np.pi*rand[1]),0) for rand in randarr])
    return Bodies(pos, vel, radius = RADIUS, dt=DT )

def randomBodiesBlackHole(num):
    vel=np.zeros((num,3))
    pos = (np.random.rand(num, 3))
    for i in range(0,num):
        pos[i][-1]=0
        (pos[i][0],pos[i][1])=(pos[i][0]*STARTSIZE*np.cos(2*np.pi*pos[i][1]),pos[i][0]*STARTSIZE*np.sin(2*np.pi*pos[i][1]))
        vel[i][0]=pos[i][1]*np.sqrt(G*m*N/STARTSIZE)/np.sqrt((pos[i][0])**2+(pos[i][1])**2)
        vel[i][1]=-pos[i][0]*np.sqrt(G*m*N/STARTSIZE)/np.sqrt((pos[i][0])**2+(pos[i][1])**2)
    print(pos.shape)
    print(np.array([[0,0,0]]).shape)
    pos2 = np.concatenate((np.array([[0,0,0]]), pos), axis=0)
    vel2 = np.concatenate((np.array([[0,0,0]]), vel), axis=0)
    mass2 = np.concatenate((M*np.ones((1,1)),m*np.ones((pos.shape[0], 1))), axis=0)
    return Bodies(pos2, vel2, mass = mass2, radius=RADIUS, dt=DT)



def main():
    
    universe = randomBodiesBlackHole(N)
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
        print(universe.impulse())
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
