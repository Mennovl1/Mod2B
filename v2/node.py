# Python object for a 3d Barnes-Hut Tree algorithm (OctTree builder)
import numpy as np
from bodies import *

ID = 0

def gB(x, n):
    'Get the n-th bit of a number x'
    return x & (1 << n) and 1 or 0

class Node:
    def __init__(self, centre, dim, identifier):
        self.centre = centre            # Centre of node
        self.com    = centre            # Centre of mass of node
        self.d      = dim               # Length/width/height of node
        self.num    = 0                 # Number of bodies in node
        self.id     = identifier        # node identifier
        self.children   = [0,0,0,0,0,0,0,0]
        self.bodies = []

    # def calcCom(self, bodies):
        # Calculate centre of mass: sum(m * r) / sum(r)
        # self.com  = np.divide(np.sum(np.multiply(bodies.pos, bodies.mass), axis=0), np.sum(bodies.pos, axis = 0)))
    

    def getOct(self, pos):
        cond = self.centre < pos    # this is a binary expression for the octant identifier
        return 1*cond[0] + 2* cond[1] + 4 * cond[2]

    def newsubNode(self, octa):
        global ID
        cx = self.centre[0] + self.d * gB(octa , 0) / 2 - self.d * (1-gB(octa, 0)) / 2
        cy = self.centre[1] + self.d * gB(octa , 1) / 2 - self.d * (1-gB(octa, 1)) / 2
        cz = self.centre[2] + self.d * gB(octa , 2) / 2 - self.d * (1-gB(octa, 2)) / 2
        centre = np.array([cx, cy, cz])
        ID += 1
        return Node(centre, self.d / 2, ID)

    def insert(self, bodies, i):
        # Recursive insertion into nodes, building a tree
        if self.num > 1:
            # If already divided into octants, insert into correct octant
            octant = self.getOct(bodies.pos[i][:])
            if not(self.children[octant]):
                self.children[octant] = self.newsubNode(octant)
            self.children[octant].insert(bodies, i)

        if self.num == 1:
            # Put existing and new particle into correct octant
            j = self.bodies[0]
            octantexisting = self.getOct(bodies.pos[j][:]) 
            octantnew = self.getOct(bodies.pos[i][:])

            self.children[octantexisting] = self.newsubNode(octantexisting)
            self.children[octantexisting].insert(bodies, j)
            self.children[octantnew] = self.newsubNode(octantnew)
            self.children[octantnew].insert(bodies, i)

        self.bodies.append(i)
        self.num += 1
    
    def __str__(self):
        tmp1 = []
        for node in self.children:
            tmp1.append(str(node))
        return "NodeID " + str(self.id) + "\n Centre " + str(self.centre) + "\n Bodies: " + str(self.bodies) + "\n Children: " + str(tmp1)


def buildTree(bodies, worldsize):
    root = Node(np.zeros((3)), worldsize, 0)
    for i in range(0, bodies.num):
        root.insert(bodies, i)

    return root