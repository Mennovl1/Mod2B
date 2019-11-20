#include "universe.h"
#include "math.h"





Universe::Universe(const bool random){
    // Constructor for our universe
    if(random){
        for(int i = 0; i < NUMSTARS; i++){
            stars[i] = randomStar(i);
        };
    } else {
        float pos1[3] = {1E2, 1E2, 0};
        float pos2[3] = {-1E2, -1E2, 0};
        float vel1[3] = {0, 0, 0};
        float vel2[3] = {0, 0, 0};
        stars[0] = Star(pos1, vel1, 0);
        stars[1] = Star(pos2, vel2, 1);
    };

    tree = buildTree(stars, WORLDSIZE);
};


void Universe::calcAcc(int starid){
    // calculate the acceleration for starid
    initAcc();
    for(int n = 0; n < NUMSTARS; n++){
        if(starid != n){  gravity((stars[starid]).pos, (stars[n]).pos, (stars[n]).mass); };
    };
};

void Universe::gravity(float a[3], float b[3], float mass){
    // Add the gravity effect of star b on star a
    float divisor = normsq(b, a);
    divisor = divisor * divisor * divisor;
    for(int i = 0; i < 3; i++){
        acc[i] += G * mass * (b[i] - a[i]) / divisor;
    };
};

void Universe::initAcc(){
    for(int i = 0; i < 3; i++){ acc[i] = 0; };
};


void Universe::do3LPFstep(){
    for(int n = 0; n < NUMSTARS; n++){
        LPFstep(stars[n].pos, stars[n].vel, DT / 2); // Update position
        calcAcc(n);
        LPFstep(stars[n].vel, acc, DT);     // Update velocity
        LPFstep(stars[n].pos, stars[n].vel, DT /2);  // Update position
    };
};

void LPFstep(float cur[3], volatile float dot[3], float dt){
    // Do one time step, without the surrounding function equivalent to Euler Forward
    for(int i = 0; i < 3; i++){
        cur[i] = cur[i] + dot[i] * dt;
    };
};

float normsq(float a[3], float b[3]){
    float d = sqrt((a[0] - b[0])*(a[0] - b[0]) +
              (a[1] - b[1])*(a[1] - b[1]) +
              (a[2] - b[2])*(a[2] - b[2]));
    return d;
};