from bodiesJulian import *
from Spiralsimulationcorrect import *



def genfile(body, name):
    text_file = open("Mod2B/v3/" + name + ".txt", "w")
    text_file.write(str(body.num) + "\n")   

    for i in range(0, body.num):
        line = str(body.mass[i][0]) + "," + str(body.pos[i][0]) + "," + str(body.pos[i][1]) + "," + str(body.pos[i][2]) + "," + str(body.vel[i][0]) + "," + str(body.vel[i][1]) + "," + str(body.vel[i][2]) + "\n"
        text_file.write(line)   
    
    text_file.close()




if False:
    for num in [10,500,1000,2000,5000,10000,15000,20000,40000,60000,80000,100000,200000]:
        res = randombodiesUnif(num)
        genfile(res, str(num))
else:
    res = SpiralGalaxyBlackHole3D(100000)
    # res = RBDonutBlackHole(5000)
    genfile(res, "input")

