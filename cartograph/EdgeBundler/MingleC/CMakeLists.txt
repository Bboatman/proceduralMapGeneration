cmake_minimum_required(VERSION 3.5)
project(MingleC)

set(CMAKE_VERBOSE_MAKEFILE ON)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

add_subdirectory(ann_1.1.2)

set(SOURCE_FILES main.cpp main.h EdgeBundler.cpp EdgeBundler.h EdgeBundleTree.cpp EdgeBundleTree.h Util.cpp Util.h)
add_executable(MingleC ${SOURCE_FILES})
target_link_libraries(MingleC LINK_PUBLIC ann)