import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from copy import deepcopy as dc
from Star import Star
from universe import Universe

#Parameters:
WIDTH = 1.0
HEIGHT = 1.0
RADIUS = 0.01
RHO = 1/(4*np.pi/3*0.01**3)
TRACE = False
SEED = "monoszijnsuf"
np.random.seed(sum(ord(char) for char in SEED))


def impossiblepos(val1, val2):
    return np.sqrt(WIDTH**2*(val1[0]-val2[0])**2 + HEIGHT**2*(val1[1]-val2[1])**2 )<= 2*RADIUS

def main():
    MODE = "random"
    fig = plt.figure()
    ax = plt.subplot(111)
    ax.set_title(MODE)

    if MODE == "random":
        N = 3
        stars = []
        randomvals = np.random.rand(N,6)
        while any(any((impossiblepos(val1,val2) and val1 is val2) for val2 in randomvals) for val1 in randomvals):
            randomvals = np.random.rand(N,4)
            print("apprehended")            
        for vals in randomvals:
            mass =4
            color = np.random.rand(3)
            stars += [Star( (WIDTH*0.5*(vals[0]-0.5), HEIGHT*0.5*(vals[1]-0.5)), (0.00*vals[2],0.00*vals[3]), mass = mass, facecolor = color)]

    universe = Universe(stars, ax, dt=5e-3, trace = TRACE)
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





    
