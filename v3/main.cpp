#include <iostream>
#include <fstream>
#include <ctime>
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
const float TIME = 10 * DT;
std::vector<Node> NODELIST;

// const char SEED[16] = "Mono's zijn suf";

std::string datetime()
{
    time_t rawtime;
    struct tm * timeinfo;
    char buffer[80];

    time (&rawtime);
    timeinfo = localtime(&rawtime);

    strftime(buffer,80,"%d-%m-%Y %H-%M-%S",timeinfo);
    return std::string(buffer);
}

float normsq(float a[3], float b[3]){
    float d = sqrt((a[0] - b[0])*(a[0] - b[0]) +
              (a[1] - b[1])*(a[1] - b[1]) +
              (a[2] - b[2])*(a[2] - b[2]));
    return d;
};

void firstline(Star starlist[], std::fstream &csvfile){
    csvfile << NUMSTARS << "," << DT << "," << TIME << "," << WORLDSIZE << "," << SPEEDRANGE << "," << THETA;
    for(int i = 0; i < NUMSTARS; i++){
        csvfile << "," << starlist[i].mass;
    };
    csvfile << "\n";
};

void appendstep(float time, Star starlist[], std::fstream &csvfile){
    csvfile << time;
    for(int i = 0; i < NUMSTARS; i++){
        csvfile << "," << starlist[i].pos[0] << "," << starlist[i].pos[1] << "," << starlist[i].pos[2];
    };
    csvfile << "\n";
};

// void consoleorcustom(bool setting){
//     G = 6.67408;
    
//     if(setting){
//         std::cout << "Stars to simulate: ";
//         std::cin >> NUMSTARS;
//         std::cout << "\nTimestep size (recommended 1e-9): ";
//         std::cin >> DT;
//         std::cout << "\nSize of the world (Milkyway is 1e3): ";
//         std::cin >> WORLDSIZE;
//         std::cout << "\nVelocities of the stars (Milkyway orbit ~8e8): ";
//         std::cin >> SPEEDRANGE;
//         std::cout << "\nTree code parameter theta (recommended 0.8): ";
//         std::cin >> THETA;
//         std::cout << "\nDo you want to use treecode (true/false): ";
//         std::cin >> TREE;

//     } else {
//         NUMSTARS = 100;
//         DT = 1e-9;
//         WORLDSIZE = 1e3;
//         SPEEDRANGE = 8e8;
//         THETA = 0.8;
//         TREE = true;
        
//     };
// };

int main(){
    // srand(201);
    // consoleorcustom(true);
    
    float t = 0;
    std::fstream csvfile;
    std::string fname = "results/" + datetime() + ".txt";
    csvfile.open(fname, std::ios::out);
    Universe world = Universe(true);
    firstline(world.stars, csvfile);

    while(t < TIME){
        appendstep(t, world.stars, csvfile);
        world.do3LPFstep();
        std::cout << t << "\n";
        t += DT;
    };
    appendstep(t, world.stars, csvfile);

    return 0;
};

