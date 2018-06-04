cmake_minimum_required(VERSION 3.7)
project(fib_huge_mod)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static -Wall -O2")

set(SOURCE_FILES fib_huge_mod.cpp)
add_executable(fib_huge_mod ${SOURCE_FILES})