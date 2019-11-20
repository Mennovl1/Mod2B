#include <iostream>
#include <cstdlib>
#include <string>
#include <vector>
#include "star.h"
#include "node.h"
#include "star.cpp"
#include "node.cpp"
#include "universe.h"
#include "universe.cpp"
#include "main.h"


const bool RANDOM = true;
std::vector<Node> NODELIST;
// const char SEED[16] = "Mono's zijn suf";


int main(){
    srand(201);
    
    std::cout << "Starting";
    Universe world = Universe(true);
    float posx1 = (world.stars[1]).pos[0];
    world.do3LPFstep();
    float posx2 = (world.stars[1]).pos[0];
    std::cout << "\n posx1 = " << posx1 << "\n posx2 = " << posx2 << "\n Difference = " << posx1 - posx2 << "\n Done";
    return 0;
};
