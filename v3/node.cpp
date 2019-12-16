#include <iostream>
#include <cstring>
#include <vector>
#include <memory>
#include <algorithm>
#include "main.h"
#include "star.h"
#include "node.h"
#include "universe.h"

Node::Node(){
    // Constructor, initialize everything to 0, except for the NodeId, which is based on the global nodecounter
    for(int i = 0; i < 3; i++){
        centre[i] = 0;
        com[i] = 0;
    };
    radius = 0; level = 0; nodeId = NodeCounter; NodeCounter += 1;
};

void Node::freechildren(){
    // A destructor for the children of the node, since we manually allocated memory for each node
    firstchild = nullptr;
    if(subdivided){
        for(int i = 0; i < 8; i++){
            if(children[i]){
                if (ChildrenNodes[i] == NULL){ return; };
                ChildrenNodes[i]->freechildren();
                delete ChildrenNodes[i];
                ChildrenNodes[i] = nullptr;

            };
        };
    };
};

Node copyNode(const Node &copy){
    // Because we want to copy the node, we should also copy the value that the point points to, instead of just copying the pointer. Otherwise different trees might contain the same subnodes
    Node newNode = Node();
    std::memcpy(&newNode, &copy, sizeof(Node));
    for(int i = 0; i < 8; i++){ 
        newNode.children[i] = copy.children[i];
        if(newNode.children[i]){ 
            newNode.ChildrenNodes[i] = new Node;
            *newNode.ChildrenNodes[i] = copyNode(*copy.ChildrenNodes[i]);
        } else {
            newNode.ChildrenNodes[i] = nullptr;
        };    
    };
    return newNode;
};

void Node::setCentre(double c[3]){
    // Update the centre of the node to the given position
    for(int i = 0; i < 3; i++){
        centre[i] = c[i];
    };
};

void Node::setLevel(uint lvl){level = lvl;};    // Update the level of the current node
void Node::setRadius(double r){radius = r;};     // Update the radius of the current node

uint Node::getOctant(double starpos[3]){
    // Return the octant of the given postion
    uint oct = 0; bool cond[3] = {false, false, false};
    for(int i = 0; i < 3; i ++){
        cond[i] = (centre[i] < starpos[i]);
    };
    oct = cond[0] + 2 * cond[1] + 4 * cond[2];
    return oct;
};

double Node::CalcCentre(uint octant, int i){
    // Construct the new centre, due to our octant definition we can use a bitwise comparison: ((octant >> i) & 1)
    bool left =  ((octant >> i) & 1);
    return centre[i] +  left * radius - (1 - left) * radius;
};

void Node::updateCOM(Star* star){
    // Update centre of mass, and mass itself
    double newcom[3];
    double newmass = mass + star->mass;
    if(newmass != 0){
        for(int i = 0; i < 3; i++){
            com[i] = (com[i] * mass + star->pos[i] * star->mass) / newmass;
    };};
    mass = newmass;
};
    
void Node::newChild(uint octant){
    // Generate a new subnode of current node
    double newcentre[3];
    for(uint i = 0; i < 3; i++){
        newcentre[i] = CalcCentre(octant, i);
    };

    ChildrenNodes[octant] =  new Node();
    ChildrenNodes[octant]->setCentre(newcentre);
    ChildrenNodes[octant]->setRadius(radius /2);
    ChildrenNodes[octant]->setLevel(level + 1);
    children[octant] = true;
};

void Node::insert(Star* star){
    // Insert a star into the node, and if necessary further divide this node up into smaller parts
    if(num > 1){
        // This node is already divided, thus determine the correct octant, and insert it there
        uint octant = getOctant(star->pos);
        if(!children[octant]){
            newChild(octant);
        };
        ChildrenNodes[octant]->insert(star);
    };
    if(num == 1){
        // There is already a star here, but the node is not divided further yet. Start dividing the node into smaller parts
        uint octantex = getOctant(firstchild->pos);
        uint octantnew= getOctant(star->pos);
        // Build new octants
        if (octantex != octantnew){
            newChild(octantex);
            };
        newChild(octantnew);
        // Insert into the new octants
        ChildrenNodes[octantex]->insert(firstchild); 
        ChildrenNodes[octantnew]->insert(star);
        subdivided = true;
    };

    firstchild = star;
    updateCOM(star);
    num += 1;
};

std::vector<double> Node::calcForce(Star targetStar){
    // Calculate the forces on the targetStar using the Barnes Hut tree
    std::vector<double> acc;

    if (num == 1){
        // If there is only one star in this node, calculate the gravity caused by this star
        Star* otherStar = firstchild;
        if(firstchild->id != targetStar.id){
            acc = gravity(targetStar.pos, firstchild->pos, firstchild->mass);
        } else {
            acc = {0,0,0};
        };
    } else{
        double r = normsq(targetStar.pos, com);
        double d = radius * 2;
        if (d/r < THETA){
            // Use this node for the approximation
            acc = gravity(targetStar.pos, com, mass);
        } else {
            // Ratio is within current distance, go deeper in the tree
            for(int i = 0; i < 3; i++){ acc.push_back(0); }; // initialization
            for(int i = 0; i < 8; i++){
                if(children[i]){
                    std::vector<double> res = ChildrenNodes[i]->calcForce(targetStar);
                    for(int j = 0; j < 3; j++){ acc.at(j) += res.at(j); };
                };
            };
        };
    };
    
    return acc;
};

Node buildTree(Star* strlist[], const double worldsize){
    // Generate a new tree with the given star list
    Node root = Node();
    root.setRadius(worldsize / 2);
    for(int i = 0; i < NUMSTARS; i++){
        root.insert(strlist[i]);
    };
    return root;
};

Node renewTree(Star* strlist[], Node &tree, const double worldsize){
    // Clear the old tree, and generate a new tree, with the new star list
    tree.freechildren();
    NodeCounter = 0;
    return buildTree(strlist, worldsize);
};
