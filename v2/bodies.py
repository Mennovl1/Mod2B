import numpy as np
import copy as cp
from num_alg import *


DT = 1000
G = 6.67E-11
RHO = 1/(4*np.pi/3*(5.51E3)**3)

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