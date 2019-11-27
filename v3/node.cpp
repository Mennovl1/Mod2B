#include <iostream>
#include <vector>
#include <memory>
#include <algorithm>
#include "main.h"
#include "star.h"
#include "node.h"



uint NodeCounter = 0;
uint TMP = 0;
float RADLIMIT = 1;

// Constructor, initialize everything to 0, except for the NodeId, which is based on the global nodecounter
Node::Node(){
    for(int i = 0; i < 3; i++){
        centre[i] = 0;
        com[i] = 0;
    };
    radius = 0; level = 0; nodeId = NodeCounter; NodeCounter += 1;
};

// Destructor needs to be customly defined, since we allocated memory by using "new" in newChild(), this memory needs to be freed by hand
void Node::freechildren(){
    // delete centre; delete com; delete &mass; delete &radius; delete children; delete &subdivided; delete &starList; delete &num; delete &nodeId; delete &level;
    // if(!TMP){
    //     delete &starList;
    //     TMP = 1;
    // }
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


// Copy constructor (rule of three)
// Node::Node(const Node &copy){
//     for(int i = 0; i < 3; i++){ centre[i] = copy.centre[i]; com[i] = copy.com[i]; };
//     for(int i = 0; i < 3; i++){ children[i] = copy.children[i]; ChildrenNodes[i] = copy.ChildrenNodes[i];};
//     mass = copy.mass; radius = copy.radius; subdivided = copy.subdivided; num = copy.num; nodeId = copy.nodeId; level = copy.level;
// };



// Update the centre of the current node to the given position
void Node::setCentre(float c[3]){
    for(int i = 0; i < 3; i++){
        centre[i] = c[i];
    };
};

void Node::setLevel(uint lvl){level = lvl;};    // Update the level of the current node
void Node::setRadius(float r){radius = r;};     // Update the radius of the current node

// Return the octant of the given postion
uint Node::getOctant(float starpos[3]){
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
    };};
    mass = newmass;
};
    
void Node::newChild(uint octant){
    // Generate a new subnode of current node
    float newcentre[3];
    for(uint i = 0; i < 3; i++){
        newcentre[i] = CalcCentre(octant, i);
    };
    // std::unique_ptr<Node> node = n
    // (*node).setCentre(newcentre);
    // (*node).setRadius(radius / 2);
    // (*node).setLevel(level + 1);
    ChildrenNodes[octant] =  new Node();
    ChildrenNodes[octant]->setCentre(newcentre);
    ChildrenNodes[octant]->setRadius(radius /2);
    ChildrenNodes[octant]->setLevel(level + 1);
    children[octant] = true;
};

void Node::insert(Star &star){
    if(num > 1){
        uint octant = getOctant((star).pos);
        if(!children[octant]){
            newChild(octant);
        };
        ChildrenNodes[octant]->insert(star);
    };
    if(num == 1){
        // Star* oldstar = starList.at(0);
        uint octantex = getOctant(firstchild->pos); // oldstar pos;
        uint octantnew= getOctant((star).pos);
        // Build new octants
        if (octantex != octantnew){
            newChild(octantex);
            };
        newChild(octantnew);
        // Insert into the new octants
        ChildrenNodes[octantex]->insert(*firstchild); 
        ChildrenNodes[octantnew]->insert(star);
        subdivided = true;
    };

    // starList.push_back(star);
    firstchild = &star;
    updateCOM(star);
    num += 1;
};

std::vector<float> Node::calcForce(Star targetStar){
    std::vector<float> acc;
    for(int i = 0; i < 3; i++){ acc.push_back(0); }; // initialization
    if (num == 1){
        Star* otherStar = firstchild;
        if((*otherStar).id != targetStar.id){
            float divisor = normsq((*otherStar).pos, targetStar.pos);
            std::max(divisor = divisor * divisor * divisor, RADLIMIT);
            for(int i = 0; i < 3; i++){
                acc.at(i) += G * (*otherStar).mass * ((*otherStar).pos[i] - targetStar.pos[i]) / divisor;
            };
        };
    } else{
        float r = normsq(targetStar.pos, com);
        float d = radius * 2;
        if (d/r < THETA){
            for(int i = 0; i < 3; i++){
                acc.at(i) += G * mass * (com[i] - targetStar.pos[i]) / std::max(r * r * r, RADLIMIT);
            };
            
        } else {
            for(int i = 0; i < 8; i++){
                if(children[i]){
                    std::vector<float> res = (*ChildrenNodes[i]).calcForce(targetStar);
                    for(int j = 0; j < 3; j++){ acc.at(j) += res.at(j); };
                };
            };
        };
    };
    
    return acc;
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

Node renewTree(Star strlist[], Node &tree, const float worldsize){
    tree.freechildren();

    TMP = 0;
    return buildTree(strlist, worldsize);
};
