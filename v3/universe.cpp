#include "universe.h"
#include "math.h"
#include <vector>





Universe::Universe(const bool random){
    // Constructor for our universe
    if(random){
        for(int i = 0; i < NUMSTARS; i++){
            stars[i] = randomStaruniform(i);
        };
    } else {
        float pos1[3] = {1E2, 1E2, 0};
        float pos2[3] = {-1E2, -1E2, 0};
        float vel1[3] = {0, 0, 0};
        float vel2[3] = {0, 0, 0};
        stars[0] = Star(pos1, vel1, 0);
        stars[1] = Star(pos2, vel2, 1);
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
                    std::vector<float> tmp = gravity((stars[starid]).pos, (stars[n]).pos, (stars[n]).mass); 
                    stars[starid].setAcc(tmp);
                };
            };
        }else{
            std::vector<float> res = tree.calcForce(stars[starid]);
            for(int i = 0; i < 3; i++){acc[i] = res.at(i);};
        };
    };
};

std::vector<float> Universe::gravity(float a[3], float b[3], float mass){
    // Add the gravity effect of star b on star a
    std::vector<float> acc = {0,0,0};
    float divisor = normsq(b, a);
    divisor = divisor * divisor * divisor;
    for(int i = 0; i < 3; i++){
        acc.at(i) += G * mass * (b[i] - a[i]) / divisor;
    };
    return acc;
};

void Universe::initAcc(int starid){
    for(int i = 0; i < 3; i++){ (stars[starid]).acc[i] = 0; };
};


void Universe::do3LPFstep(){
    for(int n = 0; n < NUMSTARS; n++){
        LPFstep(stars[n].pos, stars[n].vel, DT / 2); // Update position
    };
    calcAcc();
    for(int n = 0; n < NUMSTARS; n++){
        LPFstep(stars[n].vel, stars[n].acc, DT);     // Update velocity
        LPFstep(stars[n].pos, stars[n].vel, DT /2);  // Update position

        if(!stars[n].inWorld()){
            // stars[n] = randomStaruniform(stars[n].id);
        };
    };
    
    if(TREE){
        tree = renewTree(stars, tree, WORLDSIZE*10);
    };
};

float Universe::calcEnergy(){
    float energy = 0;
    for(int i = 0; i < NUMSTARS; i++){
        energy += stars[i].calcEnergy();
    };
    return energy;
};

float Universe::calcImpuls(int n){
    float impI = 0;
    for(int i = 0; i < NUMSTARS; i++){
        impI += stars[i].calcImpuls(n);
    };
    return impI;
};

std::vector<float> Universe::calcImpulsMoment(){
    std::vector<float> Ltot = {0,0,0};
    float zeros[3] = {0,0,0};
    for(int i = 0; i < NUMSTARS; i++){
        std::vector<float> tmp = stars[i].calcImpulsMoment(zeros);
        for(int j=0; j < 3; j++){ Ltot.at(j) += tmp.at(j); };
    };
    return Ltot;
};

void LPFstep(float cur[3], volatile float dot[3], float dt){
    // Do one time step, without the surrounding function equivalent to Euler Forward
    for(int i = 0; i < 3; i++){
        cur[i] = cur[i] + dot[i] * dt;
    };
};

