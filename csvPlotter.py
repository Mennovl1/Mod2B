# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:11:36 2019

@author: Julian
"""

import numpy as np
import vpython as vp
import time as time

FILE = "v3/results/100stars.txt"
RADIUS = 20

floatvec = np.vectorize(float)

def plotData(File):
    file = open(FILE, "r")
    line0 = file.readline()
    N, DT, TEND, SIZE, VELSIZE, THETA = floatvec(line0.split(",")[0:6])
    MASSES = floatvec(line0.split(",")[0:6]) 
    
    posline0 = file.readline()
    pos0 = floatvec(posline0.split(",")[1:])
    bodylist = []
    for i in range(int(N)):
        bodylist += [ vp.sphere(pos = vp.vector(*pos0[3*i:3*i+3]),
                                radius = RADIUS) ]
    posline = posline0
    while posline:
        pos = floatvec(posline.split(",")[1:])
        for i in range(int(N)):
            body = bodylist[i]
            body.pos = vp.vector(*pos[3*i:3*i+3])
            print("slowdown")
        posline = file.readline()
    file.close()
    
if __name__ == "__main__":
    plotData(FILE)
