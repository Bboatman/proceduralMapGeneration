#ifndef MINGLEC_EDGEBUNDLER_H
#define MINGLEC_EDGEBUNDLER_H

#include <vector>
#include "EdgeBundleTree.h"

// TODO: always make new edge when bundling - build binary tree (ignore coalesced)
// TODO: don't check for ungrouped in doMingle loop - more clumping?

class EdgeBundler {
    EdgeBundleTree::Edge *edges;
    const int numEdges, numNeighbors;
    double totalGain = 0;

public:
    EdgeBundler(EdgeBundleTree::Edge *edges, const int numEdges, const int numNeighbors);
    ~EdgeBundler();
    EdgeBundleTree* doMingle();
};

#endif //MINGLEC_EDGEBUNDLER_H
