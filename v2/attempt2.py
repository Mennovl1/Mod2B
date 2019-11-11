import numpy as np
import copy as cp
from vpython import *


G = 1

def update3LF(pos, vel, num, sw, dt):
    # Do one 3-leapfrog substep
    newpos = np.zeros((num, 3))
    for i in range(0, num):
        if(sw == 0):
            newpos[i][:] = pos[i][:] + vel[i][:] * dt / 2
        else:
            newpos[i][:] = pos[i][:] + vel[i][:] * dt
    return newpos


class bodies:
    def __init__(self, pos, vel, mass = 1, radius = 0.5):
        # Body initialization
        self.num = pos.shape[0]
        self.pos = pos
        self.vel = vel
        # self.acc = 
        self.dt = 0.0002
        self.mass = mass * np.ones((self.num))
        self.radius = radius * np.ones((self.num))
    
    def acc_coll(self):
        # Calculate acceleration, and check collision
        acc = np.zeros((self.num, 3))
    
        for i in range(0, self.num):
            coll = np.zeros(3)
            dist = np.add(self.pos, - self.pos[i][:])
            nrmdist = np.linalg.norm(cp.copy(dist), axis=1)
            nrmdist[i] = 999
            check = np.asarray(nrmdist <= self.radius + self.radius[i]).nonzero()
            if check[0].size:
                for n in check[0]:
                    self.collide(i, n)

            accmat = np.multiply(np.divide(dist, nrmdist**3), self.mass)
            acc[i][:] =  G * np.sum(accmat, axis=0)
        return acc


    def do3Sim(self):
        # Perform a full 3-leapfrog update
        self.pos = update3LF(self.pos, self.vel, self.num, 0, self.dt)
        accstep  = self.acc_coll()
        self.vel = update3LF(self.vel, accstep,  self.num, 1, self.dt)
        self.pos = update3LF(self.pos, self.vel, self.num, 0, self.dt)
    
    def collide(self, i, j):
        # perform an elastic collision
        n = self.pos[i][:] - self.pos[j][:]
        unit = n / np.linalg.norm(n)            # Normed vector connecting 2 sphere centres
        dv = self.vel[i][:] - self.vel[j][:]
        self.vel[i][:] = np.add(self.vel[i][:], 2 * unit * np.dot(unit, dv) / (self.mass[i] * (1/self.mass[i] + 1/self.mass[j])))
        # self.vel[j][:] = np.add(self.vel[j][:], 2 * unit * np.dot(unit,-dv) / (self.mass[j] * (1/self.mass[i] + 1/self.mass[j])))
        
    



def main():
    pos = np.array([[1, 1, 1], [-1, -1, 1], [1, 2, -1]])
    vel = np.zeros((3, 3))
    universe = bodies(pos, vel)

    planet = []

    for i in range(0, universe.num):
        planet.append(sphere(pos=vector(*(universe.pos[i][:])), radius = universe.radius[i], color=color.red))

    while True:
        universe.do3Sim()

        for i in range(0, universe.num):
            planet[i].pos = vector(*(universe.pos[i][:]))

        

if __name__ == "__main__":
    main()
