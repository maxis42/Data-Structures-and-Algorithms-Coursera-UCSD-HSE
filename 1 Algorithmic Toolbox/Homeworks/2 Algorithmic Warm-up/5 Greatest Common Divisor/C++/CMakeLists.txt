cmake_minimum_required(VERSION 3.7)
project(gcd)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static -Wall -O2")

set(SOURCE_FILES gcd.cpp)
add_executable(gcd ${SOURCE_FILES})