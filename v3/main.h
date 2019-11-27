#ifndef NUMSTARS
#define  NUMSTARS 100000
#endif

#ifndef DT
#define DT 0.000001
#endif

#ifndef WORLDSIZE
#define WORLDSIZE 1E6
#endif

#ifndef SPEEDRANGE
#define SPEEDRANGE 8E8
#endif

#ifndef THETA
#define THETA 0.8
#endif

#ifndef TREE
#define TREE true
#endif

#ifndef G
#define G 6.67408E10
#endif

#ifndef MAIN_H
#define MAIN_H



#include "node.h"

// int NUMSTARS;
// double DT;
// double WORLDSIZE;
// float SPEEDRANGE;
// float THETA;
// float TIME;
// bool TREE;
// float G;

// Node buildtree();
std::string datetime();
float normsq(float a[3], float b[3]);
void appendstep(float time, Star starlist[], std::fstream &csvfile);
void firstline(Star starlist[], std::fstream &csvfile);
void consoleorcustom(bool setting);
int main();

#endif // MAIN_H
