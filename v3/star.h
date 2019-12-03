#ifndef STAR_H
#define STAR_H

class Star{
    public:
        float pos[3];
        float vel[3];
        float acc[3];
        float mass;
        float radius;
        uint id;
        Star(float position[3], float velocity[3], uint identity);
        Star();
        void setMass(float newmass);
        void setAcc(std::vector<float> newAcc);
        bool inWorld();
        float calcEnergy();
        float calcImpuls(int i);
        std::vector<float> calcImpulsMoment(float reference[3]);
};

Star randomStar(uint id);
Star randomStaruniform(uint id);

#endif // STAR_H