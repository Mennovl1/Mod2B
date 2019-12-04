#include <iostream>
#include <cstdlib>
#include <cmath>
#include "main.h"
#include "star.h"

#define PI 3.14159265

Star::Star(float position[3], float velocity[3], uint identity){
    for(int i = 0; i < 3; i++){
        pos[i] = position[i];
        vel[i] = velocity[i];
        acc[i] = 0;
        mass = 20;
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

void Star::setMass(float newmass){
    mass = newmass;
};

void Star::setAcc(std::vector<float> newAcc){
    for(int i = 0; i < 3; i++){ acc[i] = newAcc.at(i); };
};

bool Star::inWorld(){
    float zeros[3] = {0,0,0};
    return (normsq(pos, zeros) < WORLDSIZE);
};

float Star::calcEnergy(){
    float zeros[3] = {0,0,0};
    float absvel = normsq(vel, zeros);
    return 0.5 * mass * absvel * absvel;
};


float Star::calcImpuls(int i){
    return mass * vel[i];
};

std::vector<float> Star::calcImpulsMoment(float reference[3]){
    float r[3]; float p[3]; std::vector<float> L = {0,0,0};
    for(int i = 0; i < 3; i++){
        r[i] = abs(pos[i] - reference[i]);
        p[i] = mass * vel[i];
    };
    L.at(0) = r[1] * p[2] - r[2] * p[1];
    L.at(1) = r[2] * p[0] - r[0] * p[2];
    L.at(2) = r[0] * p[1] - r[1] * p[0];
    return L;
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

Star randomStaruniform(uint id){
    float randpos[3]; float randvel[3]; float randterm[2];
    randpos[2] = 0; randvel[2] = 0; float zeros[3] = {0,0,0};
    float randmass = 20 + 20 * (static_cast<float>(rand()) / RAND_MAX);
    // float test = rand();

    for(int i = 0; i < 2; i++){ randterm[i] = (static_cast<float>(rand()) / RAND_MAX + 0.01); };

    randpos[0] = randterm[0] * WORLDSIZE * cos(2 * PI * randterm[1]); // r * cos(2 pi theta)
    randpos[1] = randterm[0] * WORLDSIZE * sin(2 * PI * randterm[1]);

    randvel[0] = randpos[1] * sqrt(G * randmass * NUMSTARS / WORLDSIZE) / normsq(randpos, zeros);
    randvel[1] =-randpos[0] * sqrt(G * randmass * NUMSTARS / WORLDSIZE) / normsq(randpos, zeros);
    Star newstar = Star(randpos, randvel, id);
    newstar.setMass(randmass);
    return newstar;
};