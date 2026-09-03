#include <gtest/gtest.h>

#include <string_view>

#include "fcs/version.hpp"

TEST(VersionTest, IsNonEmpty) {
  EXPECT_FALSE(std::string_view{fcs::version()}.empty());
}
