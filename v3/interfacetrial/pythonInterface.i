// SWIG interface
%module pythonInterface
%{
    #include <vector>
    #include "math.h"
    #include "main.h"
    #include "star.h"
    #include "node.h"
    #include "universe.h"
    #include "pythonInterface.h"
%}

%include "main.h"
%include "star.h"
%include "node.h"
%include "universe.h"
%include "pythonInterface.h"

%include "main.cpp"
%include "star.cpp"
%include "node.cpp"
%include "universe.cpp"
%include "pythonInterface.cpp"

// %include "node.cpp"