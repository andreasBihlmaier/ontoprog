cmake_minimum_required(VERSION 2.8.9)

project(ontoprog_cpp_test CXX)


SET(CMAKE_CXX_COMPILER "g++-4.8")
set(CMAKE_CXX_FLAGS "-std=c++11 -Wall -Wextra")


file(GLOB ONTOPROG_SRCS src/*.cpp)
include_directories(include)

add_library(ontoprog_cpp SHARED
  ${ONTOPROG_SRCS}
)



set(BIN main)
set(BIN_SRCS main.cpp)

add_executable(${BIN} ${BIN_SRCS})
target_link_libraries(${BIN} ontoprog_cpp)
