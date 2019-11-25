from copy import deepcopy as dc
import numpy as np


def Zero(r):
    return 0*r

class Universe:
    def __init__(self, bodyList, dt = 1e7, G = 6.67408e-11, Fext = Zero ):
        self.bodyList = dc(bodyList)
        self.dt = dt
        self.G = G
        self.Fext = Fext
        self.objList = []
        for body in self.bodyList:
            self.objList +=[body.draw()]
        
        self.r = np.array([body.pos for body in self.bodyList])


    def step(self):
        for i in range(len(self.bodyList)):
            body = self.bodyList[i]
            body.pos = dc(body.pos+body.vel*self.dt)
            tempBodyList = dc(self.bodyList)
            tempBodyList.pop(i)
            body.vel = body.vel + self.G*sum(list( otherBody.mass*(otherBody.pos-body.pos)/np.linalg.norm(otherBody.pos-body.pos) for otherBody in tempBodyList)) + 1/body.mass*self.Fext(body.pos)

        
    def draw(self):
        for i in range(len(self.objList)):
            obj = self.objList[i]
            obj.visible = False
        self.objList = []
        for j in range(len(self.bodyList)):
            body = self.bodyList[j]
            self.objList += [body.draw()]
            
            
    def update(self):
        self.step()
        return self.draw()
