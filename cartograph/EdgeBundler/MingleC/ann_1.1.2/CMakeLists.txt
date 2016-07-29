cmake_minimum_required(VERSION 3.5)
project(ann_1_1_2)

include_directories(include)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
    include/ANN/ANN.h
    include/ANN/ANNperf.h
    include/ANN/ANNx.h
    src/ANN.cpp
    src/bd_fix_rad_search.cpp
    src/bd_pr_search.cpp
    src/bd_search.cpp
    src/bd_tree.cpp
    src/bd_tree.h
    src/brute.cpp
    src/kd_dump.cpp
    src/kd_fix_rad_search.cpp
    src/kd_fix_rad_search.h
    src/kd_pr_search.cpp
    src/kd_pr_search.h
    src/kd_search.cpp
    src/kd_search.h
    src/kd_split.cpp
    src/kd_split.h
    src/kd_tree.cpp
    src/kd_tree.h
    src/kd_util.cpp
    src/kd_util.h
    src/perf.cpp
    src/pr_queue.h
    src/pr_queue_k.h
#    test/ann_test.cpp
#    test/rand.cpp
#    test/rand.h
        )

add_library(ann STATIC ${SOURCE_FILES})

target_include_directories (ann PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/include)

add_executable(ann2fig ${SOURCE_FILES} ann2fig/ann2fig.cpp)
add_executable(annsample ${SOURCE_FILES} sample/ann_sample.cpp)