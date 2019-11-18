#ifndef STAR_H
#define STAR_H

class Star{
    public:
        long pos[3];
        long vel[3];
        long acc[3];
        long mass;
        long radius;
        uint id;
        Star(long position[3], long velocity[3], uint identity);
        Star();
};

Star randomStar(uint id);

#endif // STAR_H