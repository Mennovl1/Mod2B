import numpy as np
import matplotlib.pyplot as plt

FILE = "/home/menno/Documents/Studie/Modelleren B/Mod2B/v3/results/theta_errors.txt"
# rc('text', usetex=True)
# rc('font', size=20)

file = open(FILE, "r")
line = file.readline()

Nlist = []
thetalist = []
errorList = []
timelist = []

floatvec = np.vectorize(float)

while line:
    N, THETA, E, T = floatvec(line.split(",")[0:4])
    Nlist.append(N)
    thetalist.append(THETA)
    errorList.append(E)
    timelist.append(T)
    line = file.readline()

print('Start plotting')

figTH = plt.figure()
figE = plt.figure()

clist = ["ob", "og", "or", "ok", "om", "o","oy"]

for i in range(0,len(thetalist)):
    plt.figure(2)
    plt.plot(Nlist[i], timelist[i], clist[i % (len(clist))])
    if errorList[i] > 0:
        plt.figure(1)
        plt.plot(Nlist[i],timelist[i],clist[i % (len(clist))])
        
plt.figure(2)
plt.legend(thetalist[0:len(clist)])
plt.xlabel('N')
plt.ylabel('t (s)')
plt.savefig("runtime.png")

plt.figure(1)
plt.legend(thetalist[1:len(clist)])
plt.xlabel('N')
plt.ylabel('t (s)')
plt.savefig("runtime.png")