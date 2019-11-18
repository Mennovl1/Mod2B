# Python object for a 3d Barnes-Hut Tree algorithm (OctTree builder)
import numpy as np
from numba import jitclass
# from bodies import Bodies

ID = 0
STARTSIZE = 1.5E15

def gB(x, n):
    'Get the n-th bit of a number x'
    return x & (1 << n) and 1 or 0

class Node:
    def __init__(self, centre = np.zeros(3), dim = 10, identifier = 0):
        self.centre     = centre            # Centre of node
        self.com        = centre            # Centre of mass of node
        self.mass       = 0
        self.d          = dim               # Length/width/height of node
        self.num        = 0                 # Number of bodies in node
        self.id         = identifier        # node identifier
        self.sub        = False             # This node is subdivided into octants
        self.children   = [0,0,0,0,0,0,0,0]
        self.bodies     = []                # Body id's that are contained in this octant

    def calcCom(self, bodies):
        # Calculate centre of mass: sum(m * r) / sum(r)
        if self.num == 1:
            self.mass = bodies.mass[self.bodies]
            self.com = bodies.pos[self.bodies]
        else:
            self.mass = np.sum(bodies.mass[self.bodies])
            top = np.sum(np.multiply(bodies.pos[self.bodies], bodies.mass[self.bodies]), axis=0)
            self.com  = np.divide(top, self.mass)
    

    def getOct(self, pos):
        '''Return the octant pos is in'''
        cond = self.centre < pos    # this is a binary expression for the octant identifier
        return 1*cond[0] + 2* cond[1] + 4 * cond[2]

    def newsubNode(self, octa):
        '''Create a new node in the corresponding octant'''
        global ID
        cx = self.centre[0] + self.d * gB(octa , 0) / 2 - self.d * (1-gB(octa, 0)) / 2
        cy = self.centre[1] + self.d * gB(octa , 1) / 2 - self.d * (1-gB(octa, 1)) / 2
        cz = self.centre[2] + self.d * gB(octa , 2) / 2 - self.d * (1-gB(octa, 2)) / 2
        centre = np.array([cx, cy, cz])
        ID += 1
        return Node(centre, self.d / 2, ID)

    def insert(self, bodies, i):
        '''Insert body i into the node and subnodes'''
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
            self.sub = True

        self.bodies.append(i)
        self.num += 1
        self.calcCom(bodies)
    
    def __str__(self):
        # tmp1 = []
        # for node in self.children:
        #     print(node)
        return "NodeID " + str(self.id) + "\n COM: " + str(self.com) + "\n Centre " + str(self.centre) + "\n Bodies: " + str(self.bodies)


def buildTree(bodies, worldsize):
    ''' Build the tree, used for treecode '''
    root = Node(np.zeros((3)), worldsize, 0)
    for i in range(0, bodies.num):
        root.insert(bodies, i)
    return root

def treeCode(bodies):
    '''Perform a tree code calculation to find the acceleration'''

    tree = buildTree(bodies, STARTSIZE)

