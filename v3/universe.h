#ifndef UNIVERSE_H
#define UNIVERSE_H

#include "main.h"
#include "star.h"
#include "node.h"

void 3LPFstep(long dot[3], long cur[3], long dt);

class Universe{
    public:
        Star stars[NUMSTARS];
        Node tree;
        Universe(const bool random);
        void do3LPFstep();
};

#endif // UNIVERSE_H