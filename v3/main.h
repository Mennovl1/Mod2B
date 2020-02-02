#ifndef MAXSTARS
#define  MAXSTARS 1000000
#endif


#ifndef SPEEDRANGE
#define SPEEDRANGE 8E8
#endif

#ifndef PI
#define PI 3.14159265
#endif


#ifndef G
#define G 6.67408
#endif

#ifndef MAIN_H
#define MAIN_H

#include <fstream>

#include "node.h"
#include "universe.h"
#include "star.h"



int NUMSTARS = 5000;
bool TREE = true;
const bool dynamicDT = false;
double THETA = 0.8;
double DT = 5E5;
double TIME = 1000 * DT;
double EPSILON = 0;
double A = 0.05;
double M = 20;
double M_BLACK = 1000;
double WORLDSIZE = 5e7;
bool RANDOM = false;
std::string INPUT = "/home/menno/Documents/Studie/Modelleren B/Mod2B/v3/input.txt";

std::string datetime();
double normsq(double a[3], double b[3]);
void appendstep(float time, Star* starlist[], std::fstream &csvfile, bool plotpos);
void donormalsim(Universe &world, std::fstream &csvfile, bool plotPos);
void errorapprox(Universe &world, std::fstream &csvfile);
std::fstream createfile();
void firstline(Star* starlist[], std::fstream &csvfile, bool plotpos);
void thetadependence(std::fstream &csvfile);
double calcrelerror(Universe &perfworld, Universe &world);
int main();

#endif // MAIN_H
