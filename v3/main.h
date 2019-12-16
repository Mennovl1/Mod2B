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



#include "node.h"


int NUMSTARS = 10;
bool TREE = true;
double THETA = 0.8;
double DT = 1E4;
double TIME = 100 * DT;
double EPSILON = 0;
double A = 0.05;
double M = 20;
double M_BLACK = 10;
double WORLDSIZE = 5e6;
const bool RANDOM = true;

std::string datetime();
double normsq(double a[3], double b[3]);
void appendstep(float time, Star* starlist[], std::fstream &csvfile);
void firstline(Star* starlist[], std::fstream &csvfile);
void consoleorcustom(bool setting);
int main();

#endif // MAIN_H
