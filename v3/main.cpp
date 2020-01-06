#include <iostream>
#include <fstream>
#include <ctime>
#include <cstdlib>
#include <string>
#include <vector>

// Custom functions
#include "star.h"
#include "node.h"
#include "star.cpp"
#include "node.cpp"
#include "universe.h"
#include "universe.cpp"
#include "main.h"




std::string datetime()
{
    // Return a string of the current date and time
    time_t rawtime; struct tm * timeinfo; char buffer[80];
    time (&rawtime);
    timeinfo = localtime(&rawtime);
    strftime(buffer,80,"%d-%m-%Y %H-%M-%S",timeinfo);
    return std::string(buffer);
}

double normsq(double a[3], double b[3]){
    // Return the distance between position a and position b
    double d = sqrt((a[0] - b[0])*(a[0] - b[0]) +
              (a[1] - b[1])*(a[1] - b[1]) +
              (a[2] - b[2])*(a[2] - b[2]));
    return d;
};

void firstline(Star* starlist[], std::fstream &csvfile, bool plotpos){
    // First line wrapper, storing usefull information when loading the text file from python
    csvfile << NUMSTARS << "," << DT << "," << TIME << "," << WORLDSIZE << "," << SPEEDRANGE << "," << THETA << "," << plotpos;
    for(int i = 0; i < NUMSTARS; i++){
        csvfile << "," << starlist[i]->mass;
    };
    csvfile << "\n";
};


void appendstep(float time, Star* starlist[], Universe* world, std::fstream &csvfile, bool plotpos){
    csvfile << time;

    if (plotpos){
        // Store the positions of all stars to the target text file
        for(int i = 0; i < NUMSTARS; i++){
            csvfile << "," << starlist[i]->pos[0] << "," << starlist[i]->pos[1] << "," << starlist[i]->pos[2];
        };
    } else {
        // Calculate energy and momentum, and create a new line for these values in the target text file
        std::vector<double> impulsMoment = world->calcImpulsMoment();
        csvfile << "," << world->calcEnergy() << "," << world->calcImpuls(0) << "," << world->calcImpuls(1) << "," << world->calcImpuls(2) << ",";
        csvfile << impulsMoment.at(0) << "," << impulsMoment.at(1) << "," << impulsMoment.at(2);
    };

    csvfile << "\n";
};


void donormalsim(Universe &world, std::fstream &csvfile, bool plotPos){
    // Perform a simulation for the specified global time
    firstline(world.stars, csvfile, plotPos);
    float t = 0;

    while(t < TIME){
        appendstep(t, world.stars, &world, csvfile, plotPos);
        world.do3LPFstep(DT);
        std::cout << t << "\n";
        t += DT;
    };

    appendstep(t, world.stars, &world, csvfile, plotPos);
};

void errorapprox(Universe &world, std::fstream &csvfile){
    // Perform Richardson extrapolation in order to approximate the error, and write this to the target text file
    int N = 4;
    float dt = DT;
    Universe worldone = world; Universe worldtwo = world; Universe worldfour = world;

    // Since the tree is a system of pointers, make sure we copy the data, instead of just the pointer. Otherwise: "segmentation-faults incoming"
    worldone.tree = copyNode(world.tree);
    worldtwo.tree = copyNode(world.tree);
    worldfour.tree = copyNode(world.tree);

    firstline(world.stars, csvfile, false);

    // Perform all required simulations
    for(int i = 0; i < N; i++){worldone.do3LPFstep(dt); };
    for(int i = 0; i < N / 2; i++){worldtwo.do3LPFstep(2*dt); };
    for(int i = 0; i < N / 4; i++){worldfour.do3LPFstep(4*dt); };

    // Calculate the Richardson Extrapolation error approximations, and write these to the target file
    for(int i = 0; i < NUMSTARS; i++){
        for(int j = 0; j < 2; j++){
            double p    = log2(abs((worldtwo.stars[i]->pos[j] - worldfour.stars[i]->pos[j]) / (worldone.stars[i]->pos[j] - worldtwo.stars[i]->pos[j])));
            double eps  = (worldone.stars[i]->pos[j] - worldtwo.stars[i]->pos[j]) / (pow(2, p) - 1); 
            csvfile << p << "," << eps << ",";
        };
        csvfile << "\n";
    }; 
};

std::fstream createfile(){
    // Create a new text file with the current date and time as name
    std::fstream csvfile;
    std::string fname = "results/" + datetime() + ".txt";
    csvfile.open(fname, std::ios::out);
    return csvfile;
};


int main(){
    int setting = 1;    
    Universe world = Universe(true);

    if(setting == 1){
        // Do a normal simulation and save the positions
        std::fstream csvfile = createfile();
        donormalsim(world, csvfile, true);
    } else if (setting == 2) {
        // Do a normal simulation and save the conserved quantities
        std::fstream csvfile = createfile();
        donormalsim(world, csvfile, false);
    } else if (setting == 3) {
        // Calculate the error order using Richardson Extrapolation
        std::fstream csvfile = createfile();
        errorapprox(world, csvfile);
    };

    return 0;
};

