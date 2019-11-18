#include <iostream>
#include <vector>
#include "main.h"
#include "star.h"
#include "node.h"


uint NodeCounter = 0;


Node::Node(long c[3], long r, uint lvl, uint newID){
    for(int i = 0; i < 3; i++){
        centre[i] = c[i];
        com[i] = c[i];
    };
    radius = r;
    level = lvl;
    nodeId = newID;
    NodeCounter += 1;
};

uint Node::getOctant(const long starpos[3]){
    uint oct = 0; bool cond[3] = {false, false, false};
    for(int i = 0; i < 3; i ++){
        cond[i] = (centre[i] < starpos[i]);
    };
    oct = cond[0] + 2 * cond[1] + 4 * cond[2];
    return oct;
};

long Node::CalcCentre(uint octant, int i){
    // Construct the new centre, due to our octant definition we can use a bitwise comparison: ((octant >> i) & 1)
    bool left =  ((octant >> i) & 1);
    return centre[i] +  left * radius - (1 - left) * radius;
};
long Node::updateCOM(Star star){
    // Update centre of mass, and mass itself
    long newcom[3];
    long newmass = mass + star.mass;
    if(newmass != 0){
        for(int i = 0; i < 3; i++){
            com[i] = (com[i] * mass + star.pos[i] * star.mass) / newmass;
    }};
    mass = newmass;
};
    
void Node::newChild(uint octant){
    // Generate a new subnode of current node
    long newcentre[3];
    for(uint i = 0; i < 3; i++){
        newcentre[i] = CalcCentre(octant, i);
    };
    Node* node = new Node(newcentre, radius/2, level + 1, NodeCounter);
    ChildrenNodes[octant] = node;
    children[octant] = true;
};

void Node::insert(const Star star){
    if(num > 1){
        uint octant = getOctant(star.pos);
        if(!children[octant]){
            newChild(octant);
        };
        (*ChildrenNodes[octant]).insert(star);
    };
    if(num == 1){
        Star oldstar = starList.at(0);
        uint octantex = getOctant(oldstar.pos); // oldstar pos;
        uint octantnew= getOctant(star.pos);
        // Build new octants
        if (octantex != octantnew){
            newChild(octantex);
            };
        newChild(octantnew);
        // Insert into the new octants
        (*ChildrenNodes[octantex]).insert(oldstar); 
        (*ChildrenNodes[octantnew]).insert(star);
        subdivided = true;
    };

    starList.push_back(star);
    updateCOM(star);
    num += 1;
};


Node buildTree(Star strlist[], const long WORLDSIZE){
    long zero[3] = {0, 0, 0};
    Node root = Node(zero, WORLDSIZE / 2, 0, 0);
    for(int i = 0; i < NUMSTARS; i++){
        root.insert((strlist[i]));
    };
    return root;
};