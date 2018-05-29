cmake_minimum_required(VERSION 3.7)
project(fib_sum_last_digit)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static -Wall -O2")

set(SOURCE_FILES fib_sum_last_digit.cpp)
add_executable(fib_sum_last_digit ${SOURCE_FILES})