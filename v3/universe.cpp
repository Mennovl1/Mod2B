#include "universe.h"
#include "star.h"
#include "math.h"

#include <vector>
#include <string>
#include <fstream>
#include <string>
#include <cstring>
#include <iostream>
// #include <PASL>

Universe::Universe(){
    acc[0] = 0; acc[1] = 0; acc[2] = 0;
};

Universe::Universe(bool random){
    // Constructor for our universe
    if(random){
        stars[0] = blackhole(0);
        for(int i = 1; i < NUMSTARS; i++){
            stars[i] = randomStaruniform(i);
        };
    };
    if(TREE){
        tree = buildTree(stars, WORLDSIZE*5);
    };
};


void Universe::calcAcc(){
    // calculate the acceleration for starid
    for(int starid = 0; starid < NUMSTARS; starid++){
        doAcc(starid);
    };
};

void Universe::doAcc(int starid){
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
}

void Universe::initAcc(int starid){
    for(int i = 0; i < 3; i++){ stars[starid]->acc[i] = 0; };
};


void Universe::do3LPFstep(double dt){
    double minR = WORLDSIZE;
    int val = 0;
    for(int n = 1; n < NUMSTARS; n++){
        LPFstep(stars[n]->pos, stars[n]->vel, dt / 2); // Update position
    };
    calcAcc();
    for(int n = 1; n < NUMSTARS; n++){
        LPFstep(stars[n]->vel, stars[n]->acc, dt);     // Update velocity
        LPFstep(stars[n]->pos, stars[n]->vel, dt /2);  // Update position

        if(!stars[n]->inWorld()){
            free(stars[n]);
            stars[n] = randomStaruniform(stars[n]->id);
        };
        double R = normsq(stars[n]->pos, stars[0]->pos);
        if(R < minR && n > 0){
            minR = R;
            val = n;
        };
    };
    
    if(TREE){
        tree = renewTree(stars, tree, WORLDSIZE*10);
    };

    if(dynamicDT){
        double zeros[3] = {0,0,0};
        DT = minR * PI / normsq(stars[val]->vel, zeros) / 2;
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

void Universe::getStarsFromFile(){
    std::string line;
    std::ifstream file(INPUT);
    bool start = false;

    if(!file){
        std::cout << "Failed to open file";
    };
    int ctr = 0;
    while(getline(file, line)){
        if(start){
            char chararr[line.size() + 1];
            strcpy(chararr, line.c_str());
            char* token = strtok(chararr, ",");
            while(token != NULL){
                double Pos[3];
                double V[3];
                double mass = atof(token); token = strtok(NULL, ",");
                Pos[0]   = atof(token); token = strtok(NULL, ",");
                Pos[1]   = atof(token); token = strtok(NULL, ",");
                Pos[2]   = atof(token); token = strtok(NULL, ",");
                V[0]     = atof(token); token = strtok(NULL, ",");
                V[1]     = atof(token); token = strtok(NULL, ",");
                V[2]     = atof(token); token = strtok(NULL, ",");

                stars[ctr] = new Star(Pos, V, ctr);
                stars[ctr]->setMass(mass);
                ctr++;
            };
        } else {
            start = true;
            NUMSTARS = std::stoi(line);
        };
        // std::cout << ctr;
    };
    M = stars[1]->mass;
    M_BLACK = stars[0]->mass;
    for(int n = 1; n < NUMSTARS; n++){
        if(!stars[n]->inWorld()){
            free(stars[n]);
            stars[n] = randomStaruniform(stars[n]->id);
        };
    };
    tree = renewTree(stars, tree, WORLDSIZE*10);
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