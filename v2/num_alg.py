# Numerical algorithm steps for our star simulations


def update3LF(pos, vel, num, sw, dt):
    # Do one 3-leapfrog substep
    newpos = np.zeros((num, 3))
    for i in range(0, num):
        if(sw == 0):
            newpos[i][:] = pos[i][:] + vel[i][:] * dt / 2
        else:
            newpos[i][:] = pos[i][:] + vel[i][:] * dt
    return newpos