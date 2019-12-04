import numpy as np
import copy as cp
from num_alg import *
#from node import *
#from numba import jit


DT = 1e-1
G = 6.67e10
#RHO = 1/(4*np.pi/3*(5.51E3)**3)*(10E4)
M = 5.972
RADIUS = 5e3

A = 5e4

class Bodies:
    def __init__(self, pos, vel, dt = DT, mass = M, radius = RADIUS):
        # Body initialization
        self.num = pos.shape[0]
        self.pos = pos
        self.vel = vel
        self.dt = dt
        self.mass = mass * np.ones((self.num, 1))
        self.radius = radius*np.ones((self.num,1))#np.cbrt(3/(np.pi*4)*self.mass/RHO)
    
    def energy(self):
        Ekin = sum(0.5*self.mass*np.linalg.norm(self.vel, axis = 1)**2)
        for i in range(0, self.num):
            # if i not in remlist:
            dist = np.add(self.pos, - self.pos[i][:])
            nrmdist = np.linalg.norm(cp.copy(dist), axis=1)
            nrmdist[i] = 999E10
            div = np.reshape(np.multiply(nrmdist, np.power(nrmdist,2)+A**2), (self.num,1))
            Umat = np.multiply( np.divide(dist, div), np.reshape(self.mass, (self.num,1)))
            U[i][:] =  G * np.sum(accmat, axis=0)
        Epot = 
        return Ekin + Epot
    
    def impulse(self):
        px = self.mass[:,0]*self.vel[:,0]
        py = self.mass[:,0]*self.vel[:,1]
        pz = self.mass[:,0]*self.vel[:,2]
        return [sum(px),sum(py),sum(pz)]
    
    def acc(self):
        '''Calculate acceleration'''
        acc = np.zeros((self.num, 3))
        for i in range(0, self.num):
            # if i not in remlist:
            dist = np.add(self.pos, - self.pos[i][:])
            nrmdist = np.linalg.norm(cp.copy(dist), axis=1)
            nrmdist[i] = 999E10
            div = np.reshape(np.multiply(np.power(nrmdist,2), np.power(nrmdist,1)+A**1), (self.num,1))
            accmat = np.multiply( np.divide(dist, div), np.reshape(self.mass, (self.num,1)))
            acc[i][:] =  G * np.sum(accmat, axis=0)
        return acc
        
    def coll(self):
        '''Check collision'''
        for i in range(0,self.num):
            dist = np.add(self.pos, - self.pos[i][:])
            nrmdist = np.linalg.norm(cp.copy(dist), axis=1)
            nrmdist[i] = 999E10
            test = np.reshape(self.radius + self.radius[i], (self.num))
            check = np.where(nrmdist <= test)
            if check[0].size:
                for n in check[0]:
                    self.elastic(i,n)
                    print("Collision",i,n)
            else:
                ""
        return

    def acc_coll(self):
        '''Calculate acceleration, and check collision'''
        acc = np.zeros((self.num, 3))
        remlist = []
    
        for i in range(0, self.num):
            # if i not in remlist:
            dist = np.add(self.pos, - self.pos[i][:])
            nrmdist = np.linalg.norm(cp.copy(dist), axis=1)
            nrmdist[i] = 999E10
                # test = np.reshape(self.radius + self.radius[i], (self.num))
                # check = np.where(nrmdist <= test)
                # if check[0].size:
                #     for n in check[0]:
                #         self.collide(i, n)
                #         # acc = cp.deepcopy(np.delete(acc, n, axis=0))
                #         # remlist.append(n)
                # else:
            div = np.reshape(np.power(nrmdist,3), (self.num,1))
            accmat = np.multiply( np.divide(dist, div), np.reshape(self.mass, (self.num,1)))
            acc[i][:] =  G * np.sum(accmat, axis=0)
        return acc


    def do3Sim(self):
        '''Perform a full 3-leapfrog update'''
        self.pos = cp.deepcopy(update3LF(self.pos, self.vel, self.num, 0, self.dt))
        #self.coll()
        accstep  = self.acc()
        self.vel = cp.deepcopy(update3LF(self.vel, accstep,  self.num, 1, self.dt))
        self.pos = cp.deepcopy(update3LF(self.pos, self.vel, self.num, 0, self.dt))

    def doBHSim(self):
        '''Perform a full 3-leapfrog update with TreeCode'''
        self.pos = cp.deepcopy(update3LF(self.pos, self.vel, self.num, 0, self.dt))
        accstep = treeCode(self)
        self.vel = cp.deepcopy(update3LF(self.vel, accstep, self.num, 1, self.dt))
        self.pos = cp.deepcopy(update3LF(self.pos, self.vel, self.num, 0, self.dt))
    
    def elastic(self, i, j):
        r = self.pos[i][:]-self.pos[j][:]
        u = float(sum((self.vel[i][:]-self.vel[j][:]))/np.linalg.norm(r)**2)
        vi = self.vel[i][:] - r*u 
        vj = self.vel[j][:] + r*u
        self.vel[i]=vi
        self.vel[j]=vj
        return 
#        r = dc(otherStar.pos-self.pos)
#        u = float((sum((self.vel-otherStar.vel)*r) )) / (np.linalg.norm(r)**2)
#        va = dc(self.vel)
#        vb = dc(otherStar.vel)
#        otherStar.vel = dc(r*u+vb)
#        self.vel = dc(va - r*u)
#        return self.vel, otherStar.vel
    
    def collide(self, i, j):
        '''Perform an inelastic collision'''
        # self.vel[i][:]  = (self.mass[i] * self.vel[i][:] + self.mass[j] * self.vel[j][:]) / (self.mass[i] + self.mass[j])
        # self.mass[i]    = self.mass[i] + self.mass[j]
        # self.pos[i][:]  = (self.pos[i][:] + self.pos[j][:]) / 2
        # self.updateradius(i)
        # self.mass       = (np.delete(self.mass, j))
        # self.radius     = (np.delete(self.radius, j))
        # self.pos        = (np.delete(self.pos, j, axis=0))
        # self.vel        = (np.delete(self.vel, j, axis=0))
        # self.num -= 1