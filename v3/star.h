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
};

Star randomStar(uint id);

#endif // STAR_H