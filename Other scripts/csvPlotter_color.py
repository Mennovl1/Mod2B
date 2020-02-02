# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:11:36 2019

@author: Julian
"""

import numpy as np
import vpython as vp
import time as time
from PIL import ImageGrab   # PIL
from subprocess import call # for issuing commands

FILE = "C:/Users/Julian/Documents/TN&TW19-20/Modelling 2B/GitHub/v3/results/10000starsBH.txt" #False
RADIUS = 20000

if not FILE:
    filename = input("What file do you want to input? \n")
    FILE = "v3/results/" + filename + ".txt"

floatvec = np.vectorize(float)

def Bounds(scene):  # return canvas bounding box, excluding frames
    x0, y0 = 10,10   
    return (int(x0), int(y0), int(1.2*scene.width+x0), int(1.2*scene.height+y0))

def plotData(File):
    file = open(FILE, "r")
    line0 = file.readline()
    N, DT, TEND, SIZE, VELSIZE, THETA = floatvec(line0.split(",")[0:6])
    MASSES = floatvec(line0.split(",")[0:6])
    scene = vp.canvas(width = 1800/1.2, height = 1000/1.2, autoscale = False, range = 2*SIZE,background=vp.vector(0,0,0.15))
    posline0 = file.readline()
    pos0 = floatvec(posline0.split(",")[1:])
    bodylist = []
    for i in range(int(N)):
        theta = np.arctan2(pos0[3*i+1], pos0[3*i])+np.pi
        color = vp.vector(0.75-0.25*np.sin(theta),0.75-0.25*np.sin(theta+2*np.pi/3),0.75-0.25*np.sin(theta-2*np.pi/3))
        bodylist += [ vp.sphere(pos = vp.vector(*pos0[3*i:3*i+3]),
                                radius = RADIUS,color= color )]
    
    posline = posline0
    input("PRESS ENTER:")
    while posline:
        #input()
        pos = floatvec(posline.split(",")[1:])
        for i in range(int(N)):
            body = bodylist[i]
            body.pos = vp.vector(*pos[3*i:3*i+3])
        posline = file.readline()
    file.close()

def plotAndAnimateData(File):
    file = open(FILE, "r")
    line0 = file.readline()
    N, DT, TEND, SIZE, VELSIZE, THETA = floatvec(line0.split(",")[0:6])
    MASSES = floatvec(line0.split(",")[0:6])
    scene = vp.canvas(width = 1000/1.2, height = 1000/1.2, autoscale = False, range = 2*SIZE, background=vp.vector(0,0,0.15))
    posline0 = file.readline()
    pos0 = floatvec(posline0.split(",")[1:])
    bodylist = []
    for i in range(int(N)):
        theta = np.arctan2(pos0[3*i+1], pos0[3*i])+np.pi
        color = vp.vector(0.75-0.25*np.sin(theta),0.75-0.25*np.sin(theta+2*np.pi/3),0.75-0.25*np.sin(theta-2*np.pi/3))
        bodylist += [ vp.sphere(pos = vp.vector(*pos0[3*i:3*i+3]),
                                radius = RADIUS,color= color )]
    posline = posline0
    input("PRESS ENTER TO START THE COUNTDOWN:")
    for i in range(10,0,-1):
        print(i)
        time.sleep(1)
    print("GO!!!")
    

    
    ic = 0
    fnum = 0
    while posline:
        #input()
        pos = floatvec(posline.split(",")[1:])
        for i in range(int(N)):
            body = bodylist[i]
            body.pos = vp.vector(*pos[3*i:3*i+3])
        posline = file.readline()
        if (ic%1 == 0):      # grab every 20 iterations, may need adjustment
            im = ImageGrab.grab(Bounds(scene))
            num = '00'+repr(fnum)           # sequence num 000-00999, trunc. below
            im.save('img-'+num[-3:]+'.png') # save to png file, 000-999, 3 digits
            fnum +=1
        ic += 1
            
    file.close()
    #call("ffmpeg -r 20 -i img-%3d.png -vcodec libx264 -vf format=yuv420p,scale={}:{} -y movie.mp4".format(int(1.2*scene.width), int(1.2*scene.height)))
    call("ffmpeg -r 20 -i img-%3d.png -vcodec libx264 -vf format=yuv420p -y movie.mp4")
    print ("\n Movie made: movie.mp4")
    
if __name__ == "__main__":
    plotAndAnimateData(FILE)
