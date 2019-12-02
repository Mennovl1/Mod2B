#ifndef UNIVERSE_H
#define UNIVERSE_H

#include "main.h"
#include "star.h"
#include "node.h"
#include <vector>


class Universe{
    public:
        Star stars[NUMSTARS];
        Node tree;
        volatile float acc[3];
        Universe(const bool random);
        void do3LPFstep();
        void calcAcc();
        void initAcc(int starid);
        std::vector<float> gravity(float a[3], float b[3], float mass);
        float calcEnergy();
        float calcImpuls(int i);
        std::vector<float> calcImpulsMoment();
};

void LPFstep(float dot[3], volatile float cur[3], float dt);
float normsq(float a[3], float b[3]);

#endif // UNIVERSE_H

