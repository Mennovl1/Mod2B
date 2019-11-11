import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from copy import deepcopy as dc
from Star import Star
#from universe import Universe

#Parameters:
G = 0.01
WIDTH = 1.0
HEIGHT = 1.0
RADIUS = 0.01
RHO = 1/(4*np.pi/3*0.01**3)
TRACE = True
SEED = "monoszijnsuf"
np.random.seed(sum(ord(char) for char in SEED))


def Fext(r):
    return 0*r

class Universe:
    def __init__(self, starList, axis, width = 1.0, height = 1.0, dt = 1e-2, trace = False, tag = "Tag"):
        self.starList = dc(starList)
        self.axis = axis
        #self.axis.plot([0,0,width,width,0],[0,height,height,0,0],"g")
        self.axis.axis("scaled")
        self.axis.set_xlim(0,width)
        self.axis.set_ylim(0,height)
        self.width = width
        self.height = height
        self.dt = dt
        self.trace = trace
        self.tag = tag
        self.patchlist = []
        self.tracelist = []
        self.tracedata = []
        for star in self.starList:
            self.patchlist +=[star.draw()]
        if self.trace:
            for j in range(len(self.starList)):
                data = list([[self.starList[j].pos[0]],[self.starList[j].pos[1]]])
                self.tracedata += [data]
                self.tracelist += self.axis.plot(data[0][0], data[1][0], color = self.starList[j].fc)
        for patch in self.patchlist:
            self.axis.add_patch(patch)
    def step(self):
        for star in self.starList:
            for otherStar in self.starList:
                if star.detectCollision(otherStar) and otherStar!= star:
                    #star.elastic(otherStar)
                    newStar = star.inelastic(otherStar)
                    #print(newStar)
                    self.starList += [newStar]
                    a = self.starList.index(star)
                    self.starList.pop(a)
                    b = self.starList.index(otherStar)
                    self.starList.pop(b)
        for star in self.starList:
            oldpos = dc(star.pos)
            star.pos = dc(star.pos+star.vel*self.dt)
            i = self.starList.index(star)
            tempStarList = dc(self.starList)
            tempStarList.pop(i)
            star.vel = star.vel + G*sum(list( otherStar.mass*(otherStar.pos-star.pos)/np.linalg.norm(otherStar.pos-star.pos) for otherStar in tempStarList)) + 1/star.mass*Fext(star.pos)
        if self.trace:
            for j in range(len(self.starList)):
                _pos = list(self.starList[j].pos)
                self.tracedata[j][0]+=[_pos[0]]
                self.tracedata[j][1]+=[_pos[1]]
    def draw(self):
        for j in range(len(self.starList)):
                self.patchlist[j].center = self.starList[j].pos
        if self.trace:
            for j in range(len(self.starList)):
                _line = self.tracelist[j]
                self.tracelist[j].set_data(*self.tracedata[j])
            return self.tracelist+self.patchlist
        else:
            return self.patchlist
    def update(self,i):
        self.step()
        return self.draw()

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
        N = 8
        stars = []
        randomvals = np.random.rand(N,4)
        while any(any((impossiblepos(val1,val2) and val1 is val2) for val2 in randomvals) for val1 in randomvals):
            randomvals = np.random.rand(N,4)
            print("apprehended")            
        for vals in randomvals:
            color =np.random.rand(3)
            stars += [Star( (WIDTH*vals[0],HEIGHT*vals[1]), (0.00*vals[2],0.00*vals[3]) , facecolor = color)]

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





    
