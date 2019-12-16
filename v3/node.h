#ifndef NODE_H
#define NODE_H

#include <memory>
#include "star.h"


class Node{
    public:
        double centre[3];
        double com[3];
        double mass = 0;
        double radius;
        bool children[8] = {false, false, false, false, false, false, false, false};
        bool subdivided = false;
        Node* ChildrenNodes[8] = {nullptr, nullptr, nullptr, nullptr, nullptr, nullptr, nullptr, nullptr};
        Star* firstchild = nullptr;
        int num = 0;
        uint nodeId;
        uint level;

        Node();                                     // Constructor
        void freechildren();                        // Destructor
        void setCentre(double c[3]);                // Set centre position of node
        void setLevel(uint lvl);                    // Set level of node
        void setRadius(double r);                   // Set the radius of the node
        uint getOctant(double starpos[3]);          // Return the octant of the given position
        double CalcCentre(uint octant, int i);      // Calculate the new centre position for the given octant
        void updateCOM(Star* star);                 // Calculate the centre of mass
        void newChild(uint octant);                 // Make a new childNode in the given octant
        void insert(Star* star);                    // Recursive function inserting stars into the tree
        std::vector<double> calcForce(Star TargetStar);
};

Node copyNode(const Node &copy);
Node buildTree(Star* strlist[], const double WORLDSIZE);
Node renewTree(Star* strlist[], Node* tree, const double worldsize);
uint NodeCounter = 0;

#endif // NODE_H