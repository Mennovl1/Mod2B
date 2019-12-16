#include "universe.h"
#include "math.h"
#include <vector>

Universe::Universe(const bool random){
    // Constructor for our universe
    if(random){
        for(int i = 0; i < NUMSTARS - 1; i++){
            stars[i] = randomStaruniform(i);
        };
        stars[NUMSTARS - 1] = blackhole(NUMSTARS - 1);
    } else {
        double pos1[3] = {1E2, 1E2, 0};
        double pos2[3] = {-1E2, -1E2, 0};
        double vel1[3] = {0, 0, 0};
        double vel2[3] = {0, 0, 0};
        stars[0] = new Star(pos1, vel1, 0);
        stars[1] = new Star(pos2, vel2, 1);
    };
    if(TREE){
        tree = buildTree(stars, WORLDSIZE*5);
    };
};


void Universe::calcAcc(){
    // calculate the acceleration for starid
    for(int starid = 0; starid < NUMSTARS; starid++){
        initAcc(starid);
        if (!TREE){
            for(int n = 0; n < NUMSTARS; n++){
                if(starid != n){ 
                    std::vector<double> tmp = gravity(stars[starid]->pos, stars[n]->pos, stars[n]->mass); 
                    stars[starid]->setAcc(tmp);
                };
            };
        }else{
            std::vector<double> res = tree.calcForce(*stars[starid]);
            for(int i = 0; i < 3; i++){acc[i] = res.at(i);};
            stars[starid]->setAcc(res);
        };
    };
};

void Universe::initAcc(int starid){
    for(int i = 0; i < 3; i++){ stars[starid]->acc[i] = 0; };
};


void Universe::do3LPFstep(double dt){
    for(int n = 0; n < NUMSTARS; n++){
        LPFstep(stars[n]->pos, stars[n]->vel, dt / 2); // Update position
    };
    calcAcc();
    for(int n = 0; n < NUMSTARS; n++){
        LPFstep(stars[n]->vel, stars[n]->acc, dt);     // Update velocity
        LPFstep(stars[n]->pos, stars[n]->vel, dt /2);  // Update position

        if(!stars[n]->inWorld()){
            free(stars[n]);
            stars[n] = randomStaruniform(stars[n]->id);
        };
    };
    
    if(TREE){
        tree = renewTree(stars, tree, WORLDSIZE*10);
    };
};

double Universe::calcEnergy(){
    double energy = 0;

    for(int i = 0; i < NUMSTARS; i++){
        energy += stars[i]->calcEnergy(); // Kinetic energy
        // Potential energy:
        if (EPSILON == 0){
            for(int j = 0; j < NUMSTARS; j++){
                // Gravitational potential if Gravitational softening is not used
                if(i != j){energy += G * stars[i]->mass * stars[j]->mass / normsq(stars[i]->pos, stars[j]->pos); };
            };
        } else {
            for(int j = 0; j < NUMSTARS; j++){
                // Gravitational potential if Gravitational softenting is used
                if(i != j){ energy += -G * stars[i]->mass * stars[j]->mass * (atan(normsq(stars[i]->pos, stars[j]->pos) / EPSILON) - PI / 2) / EPSILON; };
            };
        };
    };
    return energy;
};

double Universe::calcImpuls(int n){
    double impI = 0;
    for(int i = 0; i < NUMSTARS; i++){
        impI += abs(stars[i]->calcImpuls(n));
    };
    return impI;
};

std::vector<double> Universe::calcImpulsMoment(){
    std::vector<double> Ltot = {0,0,0};
    double zeros[3] = {0,0,0};
    for(int i = 0; i < NUMSTARS; i++){
        std::vector<double> tmp = stars[i]->calcImpulsMoment(zeros);
        for(int j=0; j < 3; j++){ Ltot.at(j) += abs(tmp.at(j)); };
    };
    return Ltot;
};

void LPFstep(double cur[3], volatile double dot[3], double dt){
    // Do one time step, without the surrounding function equivalent to Euler Forward
    for(int i = 0; i < 3; i++){
        cur[i] = cur[i] + dot[i] * dt;
    };
};

std::vector<double> gravity(double a[3], double b[3], double mass){
    // Add the gravity effect of star b on star a
    std::vector<double> acc = {0,0,0};
    double divisor = normsq(b, a);
    divisor = divisor * divisor * divisor + divisor * EPSILON;
    for(int i = 0; i < 3; i++){
        acc.at(i) += G * mass * (b[i] - a[i]) / divisor;
    };
    return acc;
};