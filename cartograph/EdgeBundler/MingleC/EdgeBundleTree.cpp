#include "EdgeBundleTree.h"

EdgeBundleTree::Edge::Edge(Point *s, Point *t, EdgeBundleTree::Edge *neighbors) {
    assert(s->x < t->x);
    sPoint = s;
    tPoint = t;
    sCentroid = s;
    tCentroid = t;
    bundle = this;

    children = nullptr;
    this->neighbors = neighbors;
    weight = 1;
    grouped = false;
    coalesced = false;
}

EdgeBundleTree::Edge::Edge(Point *s, Point *t, Point *sCentroid, Point *tCentroid, EdgeBundleTree::Edge **children) {
    assert(s->x < t->x);
    sPoint = s;
    tPoint = t;
    this->sCentroid = sCentroid;
    this->tCentroid = tCentroid;
    bundle = this;

    this->children = new std::vector<Edge*>(children, children + 2);
    neighbors = nullptr;
    weight = children[0]->weight + children[1]->weight;
    grouped = true;
    coalesced = false;
}

EdgeBundleTree::Edge::~Edge() {
    delete children;
}

EdgeBundleTree::EdgeBundleTree(Edge *edges, int numEdges) {
//    topBundles = new std::vector(edges, edges + numEdges);
}
EdgeBundleTree::~EdgeBundleTree() {
    delete topBundles;
}



double EdgeBundleTree::goldenSectionSearch(EdgeBundleTree::Edge &node0, EdgeBundleTree::Edge &node1) {
    return 0;
}

double EdgeBundleTree::getInkValueFromPoints(EdgeBundleTree::Edge &edge0, EdgeBundleTree::Edge &edge1, Point &sPoint,
                                             Point &tPoint) {
    return 0;
}

EdgeBundleTree::BundleReturn *EdgeBundleTree::testBundle(EdgeBundleTree::Edge &edge1, EdgeBundleTree::Edge &edge2) {
    return nullptr;
}

void EdgeBundleTree::applyBundle(EdgeBundleTree::BundleReturn &bundleReturn, EdgeBundleTree::Edge &edge1,
                                 EdgeBundleTree::Edge &edge2) {

}

void EdgeBundleTree::coalesceTree() {

}

