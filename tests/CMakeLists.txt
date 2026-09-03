add_executable(fcs_tests
  test_version.cpp
)
target_link_libraries(fcs_tests PRIVATE fcs_core GTest::gtest_main)

include(GoogleTest)
gtest_discover_tests(fcs_tests)
