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

SEED = "monoszijnsuf"
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
A = 0#.1*STARTSIZE
B = STARTSIZE
WITH = 20e4

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

def motionless(num):
    randarr = np.random.rand(num,2)
    pos = np.array([(STARTSIZE*rand[0]*np.cos(2*np.pi*rand[1]), STARTSIZE*rand[0]*np.sin(2*np.pi*rand[1]),0) for rand in randarr])
    VEL = 0
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
    pos = np.array([[(A + (B-A)*rand[0])*np.cos(2*np.pi*rand[1]),(A + (B-A)*rand[0])*np.sin(2*np.pi*rand[1]) ,np.random.normal(0,WITH) ] for rand in randarr])
    v = lambda r: np.sqrt(G*M/r+G*m*num*(r-A)/((B-A)*r))
    vel = np.array([[v(A+(B-A)*rand[0])*(-np.sin(2*np.pi*rand[1])),v(A+(B-A)*rand[0])*(np.cos(2*np.pi*rand[1])),0] for rand in randarr])
    col = np.array([[0.75-0.25*np.sin(2*np.pi*rand[1]),0.75-0.25*np.sin(2*np.pi*rand[1]+2*np.pi/3),0.75-0.25*np.sin(2*np.pi*rand[1]-2*np.pi/3)] for rand in randarr])
    radius = RADIUS*np.ones((num,1))
    pos2 = np.concatenate((np.array([[0,0,0]]), pos), axis=0)
    vel2 = np.concatenate((np.array([[0,0,0]]), vel), axis=0)
    mass2 = np.concatenate((M*np.ones((1,1)),m*np.ones((pos.shape[0], 1))), axis=0)
    col2 = np.concatenate((np.array([[0.2,0.2,0.2]]), col), axis=0)
    radius2 = np.concatenate((np.array([[5*RADIUS]]),radius), axis = 0)
    return Bodies(pos2, vel2, mass = mass2, radius=radius2, dt=DT, color = col2)

def RBDonut(num):
    randarr = np.random.rand(num,2)
    pos = np.array([[(A + (B-A)*rand[0])*np.cos(2*np.pi*rand[1]),(A + (B-A)*rand[0])*np.sin(2*np.pi*rand[1]) ,np.random.normal(0,WITH) ] for rand in randarr])
    v = lambda r: np.sqrt(G*m*num*(r-A)/((B-A)*r))
    vel = np.array([[v(A+(B-A)*rand[0])*(-np.sin(2*np.pi*rand[1])),v(A+(B-A)*rand[0])*(np.cos(2*np.pi*rand[1])),0] for rand in randarr])
    col = np.array([[0.75-0.25*np.sin(2*np.pi*rand[1]),0.75-0.25*np.sin(2*np.pi*rand[1]+2*np.pi/3),0.75-0.25*np.sin(2*np.pi*rand[1]-2*np.pi/3)] for rand in randarr])
    radius = RADIUS*np.ones((num,1))
    mass = m*np.ones((pos.shape[0], 1))
    return Bodies(pos, vel, mass = mass, radius = radius, dt=DT, color = col)


def SpiralGalaxy(num):
    alpha = -2
    r0 = 2e6
    eps = 1e-3
    randarr1 = np.random.rand(num)
    randarr2 = np.random.rand(num)
    #f_r = lambda r: 1/r0*np.exp(-r/r0)
    #f_phi = lambda r: (np.sin(phi))**2
    F_r = lambda r: 1-np.exp(-r/r0)
    F_r = np.vectorize(F_r)
    F_phi = lambda phi: 1/np.pi*(0.5*phi-0.25*np.sin(2*phi))
    F_phi = np.vectorize(F_phi)
    Finv_r = lambda p: -r0*np.log(1-p)
    Finv_r = np.vectorize(Finv_r)
    Finv_phi = lambda p: opt.newton((lambda x: F_phi(x)-p), p,tol = eps)
    Finv_phi = np.vectorize(Finv_phi)
#    p = np.arange(0.01,1,0.01)
#    plt.plot(Finv_phi(p),p)
#    x = np.arange(0,2*np.pi,0.1)
#    plt.plot(x, F_phi(x))
#    plt.show()
    rarr = Finv_r(randarr1)+0.1e6
    phiarr = Finv_phi(randarr2)
    pos = np.array([[rarr[i]*np.cos(phiarr[i]+alpha*np.log(rarr[i])),rarr[i]*np.sin(phiarr[i]+alpha*np.log(rarr[i])),0] for i in range(len(randarr1))])
    v = lambda r: np.sqrt(G*m*num*F_r(r)*np.pi*r/r)
    vel = np.array([[v(rarr[i])*(-np.sin(phiarr[i]+alpha*np.log(rarr[i]))),v(rarr[i])*(np.cos(phiarr[i]+alpha*np.log(rarr[i]))),0] for i in range(len(randarr1))])
    col = np.array([[0.75-0.25*np.sin(phiarr[i]),0.75-0.25*np.sin(phiarr[i]+2*np.pi/3),0.75-0.25*np.sin(phiarr[i]-2*np.pi/3)] for i in range(len(randarr1))])
    radius = RADIUS*np.ones((num,1))
    mass = m*np.ones((pos.shape[0], 1))
    return Bodies(pos, vel, mass = mass, radius=radius, dt=DT, color = col)



def main():
    
    universe = RBDonut(N)
    #universe = 
    print('generated random bodies')

    planet = []
    TIME = 0
    oldnum = universe.num
    
    scene2 = canvas(title='Galaxy Simulation',
     width=700, height=700,
     center=vector(0,0,0), background=vector(0,0,0.15))
    planet.append(sphere(pos=vector(*(universe.pos[0][:])),
                             radius = universe.radius[0],
                             texture="SmallBlackHole.jpg"))
    for i in range(1, universe.num):
        planet.append(sphere(pos=vector(*(universe.pos[i][:])),
                             radius = universe.radius[i],
                             color=vector(*universe.color[i][:])))
    
    input("PRESS ENTER TO START:")
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
