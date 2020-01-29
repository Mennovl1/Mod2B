#include "main.h"
#include "universe.h" 
#include "star.h"
#include "node.h"
#include <vector>


class pythonInterface {
    public:
        void doInit(double worldSize, int numStars, bool treeCode, double theta, double epsilon, double inner_radius, double massPlanet, double massBlackHole);
        void doStep(double dT);
        pythonInterface();
        std::vector<double> getStarpos(int i);

        bool exists;
        Universe world;
};