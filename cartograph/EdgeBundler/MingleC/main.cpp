#include <iostream>
#include "main.h"
#include "ANN/ANN.h"

using namespace std;

int main() {
    int	nPts;
    ANNpointArray dataPts;
    ANNpoint queryPt;
    ANNidxArray	nnIdx;
    ANNdistArray dists;
    ANNkd_tree*	kdTree;

    nPts = 100;
    queryPt = annAllocPt(4);
    dataPts = annAllocPts(nPts, 4);
    nnIdx = new ANNidx[10];
    dists = new ANNdist[10];

    kdTree = new ANNkd_tree(dataPts, nPts, 4);

    return 0;
}
