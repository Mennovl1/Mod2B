#ifndef NUMStARS
#define  NUMSTARS 100
#endif

#ifndef DT
#define DT 0.0005
#endif

#ifndef WORLDSIZE
#define WORLDSIZE 5E4
#endif

#ifndef SPEEDRANGE
#define SPEEDRANGE 8E8
#endif

#ifndef THETA
#define THETA 0.8
#endif

#ifndef TREE
#define TREE false
#endif

#ifndef G
#define G 6.67408E10
#endif

#ifndef MAIN_H
#define MAIN_H



#include "node.h"


// int NUMSTARS = 10;
// float DT = 0.0005;
float TIME = 1000 * DT;
// float WORLDSIZE = 5E5;
// float THETA = 0.8;
// bool TREE = true;

// Node buildtree();
std::string datetime();
float normsq(float a[3], float b[3]);
void appendstep(float time, Star starlist[], std::fstream &csvfile);
void firstline(Star starlist[], std::fstream &csvfile);
void consoleorcustom(bool setting);
int main();

#endif // MAIN_H
