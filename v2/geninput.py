from bodiesJulian import *
from Spiralsimulationcorrect import *



def genfile(body):
    text_file = open("Mod2B/v3/input.txt", "w")
    text_file.write(str(body.num) + "\n")   

    for i in range(0, body.num):
        line = str(body.mass[i][0]) + "," + str(body.pos[i][0]) + "," + str(body.pos[i][1]) + "," + str(body.pos[i][2]) + "," + str(body.vel[i][0]) + "," + str(body.vel[i][1]) + "," + str(body.vel[i][2]) + "\n"
        text_file.write(line)   
    
    text_file.close()



res = SpiralGalaxyBlackHole(5000)
# res = RBDonutBlackHole(5000)
genfile(res)