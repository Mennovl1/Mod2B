#include <iostream>
#include <cstdlib>
#include "main.h"
#include "star.h"

Star::Star(float position[3], float velocity[3], uint identity){
    for(int i = 0; i < 3; i++){
        pos[i] = position[i];
        vel[i] = velocity[i];
        acc[i] = 0;
        mass = 50;
        radius = 1;
    }
    id = identity;
};
Star::Star(){
    for(int i =0; i < 3; i++){
        pos[i] = 0; vel[i] = 0;
    };
    mass = 0; radius = 0; id = 0;
};


Star randomStar(uint id){
    // Create a random star in the world
    float randpos[3];
    float randvel[3];
    for(int i = 0; i < 3; i++){
        // Loop over x, y, z
        randpos[i] = rand(); randvel[i] = rand();
        randpos[i] = ((randpos[i] / RAND_MAX) - 0.5) * WORLDSIZE / 2;
        randvel[i] = ((randvel[i] / RAND_MAX) - 0.5) * SPEEDRANGE/ 2;
    };
    
    return Star(randpos, randvel, id);
};