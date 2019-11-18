#include "universe.h"


void 3LPFstep(long dot[3], long cur[3], long dt){
    // Do one time step, without the surrounding function equivalent to Euler Forward
    for(int i = 0; i < 3; i++){
        cur[i] = cur[i] + dot[i] * dt;
    };
};



Universe::Universe(const bool random){
    // Constructor
    if(random){
        for(int i = 0; i < NUMSTARS; i++){
            stars[i] = randomStar(i);
        };
    } else {
        long pos1[3] = {1E2, 1E2, 0};
        long pos2[3] = {-1E2, -1E2, 0};
        long vel1[3] = {0, 0, 0};
        long vel2[3] = {0, 0, 0};
        stars[0] = Star(pos1, vel1, 0);
        stars[1] = Star(pos2, vel2, 1);
    };

    tree = buildTree(stars, WORLDSIZE);
};


void Universe::do3LPFstep(){
    for(int n = 0; n < NUMSTARS; n++){
        3LPFstep(stars[n].pos, stars[n].vel, DT / 2); // Update position
        calcAcc();
        3LPFstep(stars[n].vel, acc, DT);     // Update velocity
        3LPFstep(stars[n].pos, stars[n].vel, DT /2);  // Update position
    };
};

