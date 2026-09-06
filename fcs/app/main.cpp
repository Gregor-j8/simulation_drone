#include <cstdio>

#include "fcs/version.hpp"

int main() {
  std::printf("simulation_drone fcs %s\n", fcs::version());
  std::puts("M0 scaffold: no flight loop yet.");
  return 0;
}
