from vpython import *
import numpy as np
from bodiesJulian import Bodies, DT
from node import *
from numba import jit
import copy as cp
import scipy as sp
import scipy.optimize as opt
import scipy.integrate as intg
import matplotlib.pyplot as plt

SEED = "monoszijnsuffer"
TREECODE = False
np.random.seed(sum(ord(char) for char in SEED))

N = 500
G = 6.67e10
STARTSIZE = 5e6 #in Gamma meter
MASS = 5.972
m = MASS
M = 1000*MASS
RADIUS = 4e4
DT = 1e0
A = 0.05*STARTSIZE
B = STARTSIZE

def sigma1(r):
    if r<A:
        return 0*r
    elif r>B:
        return 0*r
    else:
        return 1/(B-A)
    
def sigma2(r):
    return np.exp(-r)

sigma = np.vectorize(sigma1)

def intsigma(r):
    eps = 1e-5
    LOWER = 0
    return intg.quad(sigma, LOWER, r, epsrel = eps)[0]
intsigma = np.vectorize(intsigma)

def invintsigma(p):
    eps = 1e-5
    F = np.vectorize(lambda x:intsigma(x)-p)
    return opt.brentq(F,-0.1,2, rtol=eps)#For noncontinous dists
    #return opt.newton(F, p,tol = eps) #for continous dists
invintsigma = np.vectorize(invintsigma)

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

def RBDonutBlackHole(num):
    randarr = np.random.rand(num,2)
    pos = np.array([[(A + (B-A)*rand[0])*np.cos(2*np.pi*rand[1]),(A + (B-A)*rand[0])*np.sin(2*np.pi*rand[1]) ,0 ] for rand in randarr])
    v = lambda r: np.sqrt(G*M/r+G*m*num*(r-A)/((B-A)*r))
    vel = np.array([[v(A+(B-A)*rand[0])*(-np.sin(2*np.pi*rand[1])),v(A+(B-A)*rand[0])*(np.cos(2*np.pi*rand[1])),0] for rand in randarr])
    pos2 = np.concatenate((np.array([[0,0,0]]), pos), axis=0)
    vel2 = np.concatenate((np.array([[0,0,0]]), vel), axis=0)
    mass2 = np.concatenate((M*np.ones((1,1)),m*np.ones((pos.shape[0], 1))), axis=0)
    return Bodies(pos2, vel2, mass = mass2, radius=RADIUS, dt=DT)



def main():
    
    universe = RBDonutBlackHole(N)
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
        #print(universe.impulse())
        print(universe.energy())
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
    """
    print(invintsigma(0.6))
    x = np.arange(-1,3,1e-2)
    plt.plot(x,intsigma(x))
    y = np.arange(0,1,1e-2)
    plt.plot(invintsigma(y),y)
    plt.show()
    """
