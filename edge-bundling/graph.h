#ifndef GRAPH_H_
#define GRAPH_H_

#include <vector>

#include "edge.h"

class Graph {
 public:
  Graph() { }

  void AddEdge(const Edge& e) { edges_.push_back(e); }

  void Subdivide(int segments);

  bool Step(double dt);

  void Print() const;

 private:
  std::vector<Edge> edges_;
};

#endif  // GRAPH_H_
