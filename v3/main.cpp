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
    buildTree(strlist, WORLDSIZE);
    std::cout << "Done";
    return 0;
};
