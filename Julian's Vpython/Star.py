import numpy as np
from copy import deepcopy as dc
import vpython as vp

#Parameters:

RADIUS = 695510e-9  # Pm (=10^12 m)
RHO = 1.41e3        # 
TRACE = False
SEED = "monoszijnsuf"

class Body:
    def __init__(self, pos, vel, mass = 1, color="r", rho = RHO):
        self.pos = dc(np.array(pos))
        self.vel = dc(np.array(vel))
        self.mass = mass
        self.radius = 1e3*np.cbrt(3/(np.pi*4)*mass/rho)
        self.fc = color
        self.rho = rho

  
    def draw(self):
        #return vp.local_light(pos = vp.vector(*self.pos),
        #                      color = vp.vector(*self.fc))
        return vp.sphere(pos = vp.vector(*self.pos), 
                         size = vp.vector(self.radius, self.radius, self.radius),
                         color= vp.vector(*self.fc))

    
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
        return Star(pos, vel, mass = mass, color = color, rho = rho)

    
    def detectCollision(self, otherStar):
        r = np.linalg.norm(self.pos-otherStar.pos)
        return r <= self.radius+otherStar.radius

    
    def __repr__(self):
        return "Body object\nPos = {}\nvel = {}\nmass = {}\nradius = {}\n".format(self.pos, self.vel, self.mass, self.radius)
