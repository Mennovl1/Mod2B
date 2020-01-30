#include <iostream>
#include <fstream>
#include <string>
#include "main.h"

int main ()
{
  std::ifstream file("input.txt");
  std::string str;
  while (std::getline(file, str)) {
    std::cout << str << "\n";
  };
};