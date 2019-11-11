from copy import deepcopy as dc
import numpy as np


def Fext(r):
    return 0*r

class Universe:
    def __init__(self, starList, axis, width = 1.0, height = 1.0, dt = 1e-2, trace = False):
        self.G = 0.01
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
            oldpos = dc(star.pos)
            for otherStar in self.starList:
                if star.detectCollision(otherStar) and otherStar!= star:
                    star.elastic(otherStar)
            star.pos = dc(star.pos+star.vel*self.dt)
            i = self.starList.index(star)
            tempStarList = dc(self.starList)
            tempStarList.pop(i)
            star.vel = star.vel + self.G*sum(list( otherStar.mass*(otherStar.pos-star.pos)/np.linalg.norm(otherStar.pos-star.pos) for otherStar in tempStarList)) + 1/star.mass*Fext(star.pos)
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