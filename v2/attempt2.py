import numpy as np
import copy as cp
from vpython import *


G = 6.67E-11
RHO = 1/(4*np.pi/3*(5.51E3)**3)
SEED = "monoszijnsuf"
STARTSIZE = 1.5E14
STARTSPEED =  110E6
DT = 1000
RANDOM = True
np.random.seed(sum(ord(char) for char in SEED))

def update3LF(pos, vel, num, sw, dt):
    # Do one 3-leapfrog substep
    newpos = np.zeros((num, 3))
    for i in range(0, num):
        if(sw == 0):
            newpos[i][:] = pos[i][:] + vel[i][:] * dt / 2
        else:
            newpos[i][:] = pos[i][:] + vel[i][:] * dt
    return newpos

def randombodies(num):
    pos = 2 * STARTSIZE * (np.random.rand(num, 3) - 0.5)
    vel = 2 * STARTSPEED * (np.random.rand(num, 3) - 0.5)
    return bodies(pos, vel)


class bodies:
    def __init__(self, pos, vel, mass = 5.972E24):
        # Body initialization
        self.num = pos.shape[0]
        self.pos = pos
        self.vel = vel
        self.dt = DT
        self.mass = mass * np.ones((self.num, 1))
        self.radius = np.cbrt(3/(np.pi*4)*self.mass/RHO)
    
    def updateradius(self, i):
        self.radius[i] = np.cbrt(3/(np.pi*4)*self.mass[i]/RHO)

    def acc_coll(self):
        # Calculate acceleration, and check collision
        acc = np.zeros((self.num, 3))
        remlist = []
    
        for i in range(0, self.num):
            if i not in remlist:
                dist = np.add(self.pos, - self.pos[i][:])
                nrmdist = np.linalg.norm(cp.copy(dist), axis=1)
                nrmdist[i] = 999E10
                test = np.reshape(self.radius + self.radius[i], (self.num))
                check = np.where(nrmdist <= test)
                if check[0].size:
                    for n in check[0]:
                        self.collide(i, n)
                        acc = cp.deepcopy(np.delete(acc, n, axis=0))
                        remlist.append(n)
                else:
                    div = np.reshape(np.power(nrmdist,3), (self.num,1))
                    accmat = np.multiply( np.divide(dist, div), self.mass)
                    acc[i][:] =  G * np.sum(accmat, axis=0)
        return acc


    def do3Sim(self):
        # Perform a full 3-leapfrog update
        self.pos = cp.deepcopy(update3LF(self.pos, self.vel, self.num, 0, self.dt))
        accstep  = self.acc_coll()
        self.vel = cp.deepcopy(update3LF(self.vel, accstep,  self.num, 1, self.dt))
        self.pos = cp.deepcopy(update3LF(self.pos, self.vel, self.num, 0, self.dt))
    
    def collide(self, i, j):
        # perform an inelastic collision
        self.vel[i][:]  = (self.mass[i] * self.vel[i][:] + self.mass[j] * self.vel[j][:]) / (self.mass[i] + self.mass[j])
        self.mass[i]    = self.mass[i] + self.mass[j]
        self.pos[i][:]  = (self.pos[i][:] + self.pos[j][:]) / 2
        self.updateradius(i)
        self.mass       = (np.delete(self.mass, j))
        self.radius     = (np.delete(self.radius, j))
        self.pos        = (np.delete(self.pos, j, axis=0))
        self.vel        = (np.delete(self.vel, j, axis=0))
        self.num -= 1
        
    



def main():
    
    if RANDOM:
        universe = randombodies(50)
    else:
        pos = np.array([[1, 1, 1], [-1, 1, 1], [1, 2, -1]])
        vel = np.zeros((3, 3))
        universe = bodies(pos, vel)

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
