add_library(fcs_core
  src/version.cpp
)
target_include_directories(fcs_core PUBLIC include)

add_executable(fcs app/main.cpp)
target_link_libraries(fcs PRIVATE fcs_core)
