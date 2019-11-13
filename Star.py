import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from copy import deepcopy as dc

#Parameters:
G = 0.01
WIDTH = 1.0
HEIGHT = 1.0
RADIUS = 0.01
RHO = 1/(4*np.pi/3*0.01**3)
TRACE = True
SEED = "monoszijnsuf"
np.random.seed(sum(ord(char) for char in SEED))

class Star:
    def __init__(self, pos, vel, mass = 1, facecolor="r", rho = RHO):
        self.pos = dc(np.array(pos))
        self.vel = dc(np.array(vel))
        self.mass = mass
        self.radius = np.cbrt(3/(np.pi*4)*mass/rho)
        self.fc = facecolor
        self.rho = rho

        
    def draw(self):
        return plt.Circle(self.pos, radius = self.radius, fc=self.fc)

    
    def elastic(self, otherStar):
        r = dc(otherStar.pos-self.pos)
        u = float((sum((self.vel-otherStar.vel)*r) )) / (np.linalg.norm(r)**2)
        va = dc(self.vel)
        vb = dc(otherStar.vel)
        otherStar.vel = dc(r*u+vb)
        self.vel = dc(va - r*u)
        return self.vel, otherStar.vel

    
    def inelastic(self, otherStar):
        pos = (self.mass*self.pos+otherStar.mass*otherStar.pos)/(self.mass + otherStar.mass)
        vel = (self.mass*self.vel+otherStar.mass*otherStar.vel)/(self.mass + otherStar.mass)
        mass = (self.mass + otherStar.mass)
        rho = mass/(self.mass/self.rho + otherStar.mass/otherStar.rho)
        radius = np.cbrt(3/(np.pi*4)*mass/RHO)
        color = np.random.rand(3)
        return Star(pos, vel, mass = mass, facecolor = color, rho = rho)

    
    def detectCollision(self, otherStar):
        r = np.linalg.norm(self.pos-otherStar.pos)
        return r <= self.radius+otherStar.radius

    
    def __repr__(self):
        return "Star object\nPos = {}\nvel = {}\nmass = {}\nradius = {}\n".format(self.pos, self.vel, self.mass, self.radius)
