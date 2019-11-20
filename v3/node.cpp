#include <iostream>
#include <vector>
#include "main.h"
#include "star.h"
#include "node.h"


uint NodeCounter = 0;

// Constructor, initialize everything to 0, except for the NodeId, which is based on the global nodecounter
Node::Node(){
    for(int i = 0; i < 3; i++){
        centre[i] = 0;
        com[i] = 0;
    };
    radius = 0; level = 0; nodeId = NodeCounter; NodeCounter += 1;
};

// Update the centre of the current node to the given position
void Node::setCentre(float c[3]){
    for(int i = 0; i < 3; i++){
        centre[i] = c[i];
    };
};

void Node::setLevel(uint lvl){level = lvl;};    // Update the level of the current node
void Node::setRadius(float r){radius = r;};     // Update the radius of the current node

// Return the octant of the given postion
uint Node::getOctant(const float starpos[3]){
    uint oct = 0; bool cond[3] = {false, false, false};
    for(int i = 0; i < 3; i ++){
        cond[i] = (centre[i] < starpos[i]);
    };
    oct = cond[0] + 2 * cond[1] + 4 * cond[2];
    return oct;
};

float Node::CalcCentre(uint octant, int i){
    // Construct the new centre, due to our octant definition we can use a bitwise comparison: ((octant >> i) & 1)
    bool left =  ((octant >> i) & 1);
    return centre[i] +  left * radius - (1 - left) * radius;
};
void Node::updateCOM(Star star){
    // Update centre of mass, and mass itself
    float newcom[3];
    float newmass = mass + star.mass;
    if(newmass != 0){
        for(int i = 0; i < 3; i++){
            com[i] = (com[i] * mass + star.pos[i] * star.mass) / newmass;
    }};
    mass = newmass;
};
    
void Node::newChild(uint octant){
    // Generate a new subnode of current node
    float newcentre[3];
    for(uint i = 0; i < 3; i++){
        newcentre[i] = CalcCentre(octant, i);
    };
    Node* node = new Node();
    (*node).setCentre(newcentre);
    (*node).setRadius(radius / 2);
    (*node).setLevel(level + 1);
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


Node buildTree(Star strlist[], const float worldsize){
    float zero[3] = {0, 0, 0};
    Node root = Node();
    root.setRadius(worldsize / 2);
    for(int i = 0; i < NUMSTARS; i++){
        root.insert((strlist[i]));
    };
    return root;
};