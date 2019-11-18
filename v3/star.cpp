#include <iostream>
#include <cstdlib>
#include "main.h"
#include "star.h"

Star::Star(long position[3], long velocity[3], uint identity){
    for(int i = 0; i < 3; i++){
        pos[i] = position[i];
        vel[i] = velocity[i];
        acc[i] = 0;
        mass = 0;
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
    long randpos[3];
    long randvel[3];
    for(int i = 0; i < 3; i++){
        // Loop over x, y, z
        randpos[i] = rand(); randvel[i] = rand();
        randpos[i] = randpos[i] * WORLDSIZE / UINT16_MAX;
        randvel[i] = randvel[i] * SPEEDRANGE / UINT16_MAX;
    };
    
    return Star(randpos, randvel, id);
};