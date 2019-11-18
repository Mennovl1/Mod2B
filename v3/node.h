#ifndef NODE_H
#define NODE_H

#include "star.h"

class Node{
    public:
        long centre[3];
        long com[3];
        long mass = 0;
        long radius;
        bool children[8] = {false, false, false, false, false, false, false, false};
        bool subdivided = false;
        Node* ChildrenNodes[8];
        std::vector<Star> starList;
        int num = 0;
        uint nodeId;
        uint level;
        Node(long c[3], long radius, uint lvl, uint newID);
        uint getOctant(const long starpos[3]);
        long CalcCentre(uint octant, int i);
        long updateCOM(Star star);
        void newChild(uint octant);
        void insert(const Star star);
};

Node buildTree(Star strlist[], const long WORLDSIZE)

#endif // NODE_H