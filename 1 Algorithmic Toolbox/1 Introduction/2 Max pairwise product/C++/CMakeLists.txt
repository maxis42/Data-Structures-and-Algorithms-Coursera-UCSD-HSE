cmake_minimum_required(VERSION 3.7)
project(max_pairwise_product)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -static -Wall -O2")

set(SOURCE_FILES max_pairwise_product.cpp)
add_executable(max_pairwise_product ${SOURCE_FILES})