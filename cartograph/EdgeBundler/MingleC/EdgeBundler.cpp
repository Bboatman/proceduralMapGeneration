#include "EdgeBundler.h"
#include "EdgeBundleTree.h"


EdgeBundler::EdgeBundler(EdgeBundleTree::Edge *edges, int numEdges, int numNeighbors)
        : numEdges(numEdges), numNeighbors(numNeighbors), edges(edges) { }

EdgeBundler::~EdgeBundler() {

}

EdgeBundleTree* EdgeBundler::doMingle() {
    EdgeBundleTree *tree = new EdgeBundleTree(edges, numEdges);
    bool inkSaved;
    EdgeBundleTree::BundleReturn *bundleReturnArray[numNeighbors];
    do {
        inkSaved = false;
        for (int i = 0; i < numEdges; ++i) {
            EdgeBundleTree::Edge& edge = edges[i];
            if (!edge.grouped) {
                double maxInkSaved = -INFINITY;
                int maxSavingNeighborIndex = 0;
                for (int j = 0; j < numNeighbors; ++j) {
                    EdgeBundleTree::Edge& neighbor = edge.neighbors[j];
                    EdgeBundleTree::BundleReturn *bundleReturn = EdgeBundleTree::testBundle(edge, neighbor);
                    bundleReturnArray[j] = bundleReturn;
                    if (bundleReturn->inkSaved > maxInkSaved) {
                        maxInkSaved = bundleReturn->inkSaved;
                        maxSavingNeighborIndex = j;
                    }
                }
                if (maxInkSaved > 0) {
                    EdgeBundleTree::applyBundle(*bundleReturnArray[maxSavingNeighborIndex],
                                                edge,
                                                edge.neighbors[maxSavingNeighborIndex]);
                    inkSaved = true;
                }
            }
        }
        tree->coalesceTree();
    } while (inkSaved);
    return tree;
}


