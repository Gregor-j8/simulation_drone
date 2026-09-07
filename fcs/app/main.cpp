#include <cstdio>

#include "fcs/version.hpp"

int main() {
  // fputs/puts, not printf: C varargs defeat type safety
  // (cppcoreguidelines-pro-type-vararg).
  std::fputs("simulation_drone fcs ", stdout);
  std::puts(fcs::version());
  std::puts("M0 scaffold: no flight loop yet.");
  return 0;
}
