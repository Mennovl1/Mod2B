#include <vector>

#ifndef STAR_H
#define STAR_H


class Star{
    public:
        double pos[3];
        double vel[3];
        double acc[3];
        double mass;
        double radius;
        uint id;
        Star(double position[3], double velocity[3], uint identity);
        Star();
        void setMass(double newmass);
        void setAcc(std::vector<double> newAcc);
        bool inWorld();
        double calcEnergy();
        double calcImpuls(int i);
        std::vector<double> calcImpulsMoment(double reference[3]);
};

Star* randomStar(uint id);
Star* randomStaruniform(uint id);

#endif // STAR_H