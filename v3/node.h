#ifndef NODE_H
#define NODE_H

#include "star.h"

class Node{
    public:
        float centre[3];
        float com[3];
        float mass = 0;
        float radius;
        bool children[8] = {false, false, false, false, false, false, false, false};
        bool subdivided = false;
        Node* ChildrenNodes[8];
        std::vector<Star> starList;
        int num = 0;
        uint nodeId;
        uint level;

        Node();                                     // Constructor
        void setCentre(float c[3]);                 // Set centre position of node
        void setLevel(uint lvl);                    // Set level of node
        void setRadius(float r);                    // Set the radius of the node
        uint getOctant(const float starpos[3]);     // Return the octant of the given position
        float CalcCentre(uint octant, int i);       // Calculate the new centre position for the given octant
        void updateCOM(Star star);                  // Calculate the centre of mass
        void newChild(uint octant);                 // Make a new childNode in the given octant
        void insert(const Star star);               // Recursive function inserting stars into the tree
};

Node buildTree(Star strlist[], const float WORLDSIZE);

#endif // NODE_H