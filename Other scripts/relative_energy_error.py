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

rc('text', usetex=True)
rc('font', size=20)


FILE = "results/energytree.txt"
FILE2 = "results/absenergytree.txt"
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
    scene = vp.canvas(width = 1800, height = 1000, autoscale = False, range = 2*SIZE)
    posline = True
    posline2 = True

    E = 0; Pxold = 0; Pyold = 0; Pzold = 0; Lxold = 0; Lyold = 0; Lzold = 0
    listdE = []; listdPx = []; listdPy = []; listdLz = []

    posline = file.readline()
    posline2 = file2.readline()
    listT = []
    while posline and posline2:
        
        T, ENERGY, Px, Py, Pz, Lx, Ly, Lz = floatvec(posline.split(",")[0:])
        Eabs, Pxabs, Pyabs, Pzabs, Lxabs, Lyabs, Lzabs = floatvec(posline2.split(",")[1:])
        
        listT.append(T * 1e13)

        listdE.append(  abs((E - ENERGY) / Eabs))
        listdPx.append( abs((Pxold - Px) / Pxabs))
        listdPy.append( abs((Pyold - Py) / Pyabs))
        # listdPz.append( (Pzold - Pz) / Pzabs)
        # listdLx.append( (Lxold - Lx) / Lxabs)
        # listdLy.append( (Lyold - Ly) / Lyabs)
        listdLz.append( abs((Lzold - Lz) / Lzabs))

        E = cp.deepcopy(ENERGY); Pxold = cp.deepcopy(Px); Pyold = cp.deepcopy(Py)
        Pzold = cp.deepcopy(Pz); Lxold = cp.deepcopy(Lx); Lyold = cp.deepcopy(Ly); Lzold = cp.deepcopy(Lz)
        posline = file.readline()
        posline2 = file2.readline()

    file.close()
    file2.close()

    figE = plt.figure()
    plt.plot(listT[1:], listdE[1:], 'o')
    plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e'))
    plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e')) 
    plt.xlabel(r't (s)')
    plt.ylabel(r"$\epsilon$")
    plt.tight_layout()
    figE.savefig("energytree.png")

    figPx = plt.figure()
    plt.plot(listT[2:], listdPx[2:], 'o')
    plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e'))
    plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e')) 
    plt.xlabel(r't (s)')
    plt.ylabel(r"$\epsilon$")
    plt.tight_layout()
    figPx.savefig("xmomenttree.png")

    figPy = plt.figure()
    plt.plot(listT[2:], listdPy[2:], 'o')
    plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e')) 
    plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e')) 
    plt.xlabel(r't (s)')
    plt.ylabel(r"$\epsilon$")
    plt.tight_layout()
    figPy.savefig("ymomenttree.png")

    figLz = plt.figure()
    plt.plot(listT[2:], listdLz[2:], 'o')
    plt.gca().yaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e')) 
    plt.gca().xaxis.set_major_formatter(mtick.FormatStrFormatter('%.0e')) 
    plt.xlabel(r't (s)')
    plt.ylabel(r"$\epsilon$")
    plt.tight_layout()
    figLz.savefig("zmomenttree.png")





if __name__ == "__main__":
    plotData(FILE)
