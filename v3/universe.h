#ifndef UNIVERSE_H
#define UNIVERSE_H

#include "main.h"
#include "star.h"
#include "node.h"
#include <vector>


class Universe{
    public:
        Star* stars[MAXSTARS];
        Node tree;
        volatile double acc[3];
        Universe();
        Universe(const bool random);
        void do3LPFstep(double dt);
        void calcAcc();
        void initAcc(int starid);
        
        double calcEnergy();
        double calcImpuls(int i);
        std::vector<double> calcImpulsMoment();
};

void LPFstep(double dot[3], volatile double cur[3], double dt);
double normsq(double a[3], double b[3]);
std::vector<double> gravity(double a[3], double b[3], double mass);

#endif // UNIVERSE_H

