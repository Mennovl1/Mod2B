import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from universe import *
from copy import deepcopy as dc

#Parameters:

WIDTH = 1.0
HEIGHT = 1.0
RADIUS = 0.01
TRACE = True
SEED = "monoszijnsuf"

np.random.seed(sum(ord(char) for char in SEED))


class Star:
    def __init__(self, pos, vel, mass = 1, radius=0.01, facecolor="r",):
        self.pos = dc(np.array(pos))
        self.vel = dc(np.array(vel))
        self.mass = mass
        self.radius = radius
        self.fc = facecolor
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
        return "TO BE FILLED IN"
    def detectCollision(self, otherStar):
        r = np.linalg.norm(self.pos-otherStar.pos)
        return r <= self.radius+otherStar.radius
    def __repr__(self):
        return "Star object\nPos = {}\nvel = {}\nmass = {}\n".format(self.pos, self.vel, self.mass)


def impossiblepos(val1, val2):
    return np.sqrt(WIDTH**2*(val1[0]-val2[0])**2 + HEIGHT**2*(val1[1]-val2[1])**2 )<= 2*RADIUS

def main():
    MODE = "random"
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.set_title(MODE)

    if MODE == 'two stars':
        a = Star((1.5,RADIUS),(0.15,3), facecolor = "b", radius = RADIUS)
        b = Star((1.5,0.75,),(0,0), radius = RADIUS )
        stars = [a,b]
    elif MODE == "random":
        N = 4
        stars = []
        randomvals = np.random.rand(N,4)
        while any(any((impossiblepos(val1,val2) and val1 is val2) for val2 in randomvals) for val1 in randomvals):
            randomvals = np.random.rand(N,4)
            print("apprehended")
                    
        for vals in randomvals:
            color =np.random.rand(3)
            stars += [Star( (WIDTH*vals[0],HEIGHT*vals[1]), (0.00*vals[2],0.00*vals[3]) ,radius = RADIUS, facecolor = color)]

    universe = Universe(stars,ax, dt=5e-3, trace = TRACE)
    mov = anim.FuncAnimation(fig,
                                  universe.update,
                                  frames = 100,
                                  interval = 1000*universe.dt,
                                  blit = True)
    try:
        plt.show()
    except AttributeError:
        print("AtrributeError")
   
if __name__ == "__main__":
    main()





    
