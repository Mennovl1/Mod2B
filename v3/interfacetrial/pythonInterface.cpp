#include "pythonInterface.h"
#include "universe.h"

pythonInterface::pythonInterface(){
    exists = true;
    world = Universe(true);
};

void pythonInterface::doInit(double worldSize, int numStars, bool treeCode, double theta, double epsilon, double inner_radius, double massPlanet, double massBlackHole){
    WORLDSIZE = worldSize;
    NUMSTARS = numStars;
    TREE = treeCode;
    THETA = theta;
    EPSILON = epsilon;
    A = inner_radius;
    M = massPlanet;
    M_BLACK = massBlackHole;

    world = Universe(true);
};

void pythonInterface::doStep(double dT){
    world.do3LPFstep(dT);
};

std::vector<double> pythonInterface::getStarpos(int i){
    std::vector<double> res;
    for(int j = 0; j < 3; j++){
        res.at(j) = world.stars[i]->pos[j];
    };
    return res;
};


