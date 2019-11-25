#ifndef NUMSTARS
#define  NUMSTARS 3
#endif

#ifndef DT
#define DT 1E-10
#endif

#ifndef WORLDSIZE
#define WORLDSIZE 1E3
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

#ifndef MAIN_H
#define MAIN_H

#ifndef G
#define G 6.67408
#endif

#include "node.h"

// Node buildtree();
float normsq(float a[3], float b[3]);
int main();

#endif // MAIN_H
