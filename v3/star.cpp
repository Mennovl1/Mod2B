#include <iostream>
#include <cstdlib>
#include <cmath>
#include <vector>
#include "main.h"
#include "star.h"




Star::Star(double position[3], double velocity[3], uint identity){
    // Create a star with the given parameters
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
    // Create a null-valued star
    for(int i =0; i < 3; i++){
        pos[i] = 0; vel[i] = 0;
    };
    mass = 0; radius = 0; id = 0;
};

void Star::setMass(double newmass){ mass = newmass; }; // Set the mass to the given value

void Star::setAcc(std::vector<double> newAcc){
    // Update the acceleration to the given value
    for(int i = 0; i < 3; i++){ acc[i] = newAcc.at(i); };
};

bool Star::inWorld(){
    // Check if the current position is within the given worldsize for the Barnes Hut tree algorithm
    double zeros[3] = {0,0,0};
    return (normsq(pos, zeros) < WORLDSIZE*10);
};

double Star::calcEnergy(){
    // Calculate the kinetic energy of this star
    double zeros[3] = {0,0,0};
    double absvel = normsq(vel, zeros);
    return 0.5 * mass * absvel * absvel;
};


double Star::calcImpuls(int i){
    // Calculate the impuls of this star
    return mass * vel[i];
};

std::vector<double> Star::calcImpulsMoment(double reference[3]){
    // Calculate the impulse moment of this star in reference to the origin
    double r[3]; double p[3]; std::vector<double> L = {0,0,0};
    for(int i = 0; i < 3; i++){
        r[i] = abs(pos[i] - reference[i]);
        p[i] = mass * vel[i];
    };
    L.at(0) = r[1] * p[2] - r[2] * p[1];
    L.at(1) = r[2] * p[0] - r[0] * p[2];
    L.at(2) = r[0] * p[1] - r[1] * p[0];
    return L;
};

Star* randomStar(uint id){
    // Create a random star in the world
    double randpos[3];
    double randvel[3];
    for(int i = 0; i < 3; i++){
        // Loop over x, y, z
        randpos[i] = rand(); randvel[i] = rand();
        randpos[i] = ((randpos[i] / RAND_MAX) - 0.5) * WORLDSIZE;
        randvel[i] = ((randvel[i] / RAND_MAX) - 0.5) * SPEEDRANGE/ 2;
    };
    Star* newstar = new Star(randpos, randvel, id);
    return newstar;
};

Star* randomStaruniform(uint id){
    // Generate a random star that is distributed uniformly, with a stable orbit
    double randpos[3]; double randvel[3]; double randterm[2];
    randpos[2] = 0; randvel[2] = 0; double zeros[3] = {0,0,0};
    double randmass = M + M * (static_cast<double>(rand()) / RAND_MAX);

    for(int i = 0; i < 2; i++){ randterm[i] = (static_cast<double>(rand()) / RAND_MAX + A); };

    randpos[0] = randterm[0] * WORLDSIZE * cos(2 * PI * randterm[1]); // r * cos(2 pi theta) = x
    randpos[1] = randterm[0] * WORLDSIZE * sin(2 * PI * randterm[1]); // r * sin(2 pi theta) = y

    double r = normsq(randpos, zeros);
    double v = sqrt(G * ( M_BLACK * M / r + randmass * NUMSTARS * (r - A*WORLDSIZE) / ((1 - A) * WORLDSIZE * r)));
    randvel[0] = randpos[1] * v / r;
    randvel[1] =-randpos[0] * v / r;

    Star* newstar = new Star(randpos, randvel, id);
    newstar->setMass(randmass);
    return newstar;
};

Star* blackhole(uint id){
    // Return a supermassive star/black hole located at the origin
    double pos[3] = {0,0,0};
    double vel[3] = {0,0,0};
    double mass = M_BLACK * M;
    Star* newstar = new Star(pos, vel, id);
    newstar->setMass(mass);
    return newstar;
};