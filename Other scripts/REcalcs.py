# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 16:11:36 2019

@author: Julian
"""

import numpy as np
import vpython as vp
import time as time
import copy as cp
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib import rc
import scipy.stats as st

rc('text', usetex=True)
rc('font', size=20)


FILE = "Mod2B/v3/results/RichardsonExtraptree.txt"
FILE2 = "Mod2B/v3/results/RichardsonExtrapnormal.txt"
RADIUS = 20000

if False:
    filename = input("What file do you want to input? \n")
    FILE = "v3/results/" + filename + ".txt"
    filename2 = input("What are the absolute values? \n")
    FILE2 = "v3/results/" + filename2 + ".txt"

floatvec = np.vectorize(float)


def plotData(File):
    file = open(FILE, "r")
    file2 = open(FILE2, 'r')
    line0 = file.readline()
    N, DT, TEND, SIZE, VELSIZE, THETA = floatvec(line0.split(",")[0:6])
    MASSES = floatvec(line0.split(",")[0:6])
    line20 = file2.readline()

    posline = True
    posline2 = True

    posline = file.readline()
    posline2 = file2.readline()
    poslist = []; tposlist = []; plist = []; tplist = []

    while posline and posline2:
        
        p1t, xt, p2t, yt        = floatvec(posline.split(",")[0:4])
        p1, x, p2, y    = floatvec(posline2.split(",")[0:4])
        
        if abs(x) < 100 and abs(y) < 100:
            poslist.append(x); poslist.append(y)
            plist.append([p1, p2])
        if abs(xt) < 100 and abs(yt) < 100:
            tposlist.append(xt); tposlist.append(yt)
            tplist.append([p1t, p2t])
       
        posline = file.readline()
        posline2 = file2.readline()

    file.close()
    file2.close()
    
    print(np.mean(poslist))
    print(np.std(poslist))
    
    print(np.mean(plist))
    print(np.std(plist))
    
    print(np.mean(tposlist))
    print(np.std(tposlist))

    print(np.mean(tplist))
    print(np.std(tplist))


if __name__ == "__main__":
    plotData(FILE)
