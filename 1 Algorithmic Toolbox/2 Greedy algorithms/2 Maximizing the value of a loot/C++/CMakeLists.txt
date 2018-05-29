cmake_minimum_required(VERSION 3.7)
project(loot)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static -Wall -O2")

set(SOURCE_FILES loot.cpp)
add_executable(loot ${SOURCE_FILES})