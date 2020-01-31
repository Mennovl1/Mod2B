# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:11:36 2019

@author: Julian
"""

import numpy as np
import vpython as vp
import time as time

FILE = "C:/Users/Gijs Mast/Documents/Universiteit jaar 3/Modelling-B/mod2b/v3/results/v1000m1M1e6Dt1.txt" #False
RADIUS = 20000

if not FILE:
    filename = input("What file do you want to input? \n")
    FILE = "v3/results/" + filename + ".txt"

floatvec = np.vectorize(float)

def plotData(File):
    file = open(FILE, "r")
    line0 = file.readline()
    N, DT, TEND, SIZE, VELSIZE, THETA = floatvec(line0.split(",")[0:6])
    MASSES = floatvec(line0.split(",")[0:6])
    scene = vp.canvas(width = 1800, height = 1000, autoscale = False, range = 2*SIZE)
    posline0 = file.readline()
    pos0 = floatvec(posline0.split(",")[1:])
    bodylist = []
    for i in range(int(N)):
        theta = np.arctan2(pos0[3*i+1], pos0[3*i])+np.pi
        color = vp.vector(0.75-0.25*np.sin(theta),0.75-0.25*np.sin(theta+2*np.pi/3),0.75-0.25*np.sin(theta-2*np.pi/3))
        print(color)
        print(type(color))
        bodylist += [ vp.sphere(pos = vp.vector(*pos0[3*i:3*i+3]),
                                radius = RADIUS,col= color )]
    
    posline = posline0
    input()
    while posline:
        #input()
        pos = floatvec(posline.split(",")[1:])
        for i in range(int(N)):
            body = bodylist[i]
            body.pos = vp.vector(*pos[3*i:3*i+3])
            print("slowdown")
        posline = file.readline()
    file.close()
    
if __name__ == "__main__":
    plotData(FILE)
