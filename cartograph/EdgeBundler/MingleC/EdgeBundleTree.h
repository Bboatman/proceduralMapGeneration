#ifndef MINGLEC_EDGEBUNDLETREE_H
#define MINGLEC_EDGEBUNDLETREE_H

#include <vector>
#include <cmath>
#include <cassert>
#include "Util.h"

class EdgeBundleTree {

public:
    struct Edge {
//        std::vector<Point*> *S = new std::vector<Point*>(), *T = new std::vector<Point*>();
        Point *sPoint, *tPoint;
        Point *sCentroid, *tCentroid;
        Edge *bundle;  // highest parent for this edge
        std::vector<Edge*> *children;
        Edge *neighbors;
        double ink;
        int weight;
        bool grouped;
        bool coalesced;

        Edge(Point *s, Point *t, Edge* neighbors);  // for leaf nodes
        Edge(Point *s, Point *t, Point* sCentroid, Point *tCentroid, Edge **children);  // for parent nodes
        ~Edge();
    };

    typedef struct {
        Point *s, *t;
        double inkSaved;
    } BundleReturn;

    std::vector<Edge*> *topBundles;

    EdgeBundleTree(Edge *edges, int numEdges);
    ~EdgeBundleTree();
    static double getInkValueFromPoints(Edge& edge0, Edge& edge1, Point& sPoint, Point& tPoint);
    static BundleReturn* testBundle(Edge& edge1, Edge& edge2);
    static void applyBundle(BundleReturn& bundleReturn, Edge& edge1, Edge& edge2);
    void coalesceTree();

private:
    double goldenSectionSearch(Edge& node0, Edge& node1);
};


#endif //MINGLEC_EDGEBUNDLETREE_H
