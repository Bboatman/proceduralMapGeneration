#include "graph.h"

void Graph::Subdivide(int segments) {
  for (size_t i = 0; i < edges_.size(); ++i) {
    edges_[i].Subdivide(segments);
  }
}

bool Graph::Step(double dt) {
  for (size_t i = 0; i < edges_.size(); ++i) {
    Edge& p = edges_[i];
    p.ClearForces();
    p.AddSpringForces();
    for (size_t j = 0; j < edges_.size(); ++j) {
      if (i == j)
        continue;
      const Edge& q = edges_[j];
      p.AddElectrostaticForces(q);
    }
  }

  // Set done to false if any node moves > EPSILON
  bool done = true;
  for (size_t i = 0; i < edges_.size(); ++i) {
    if (edges_[i].UpdatePositions(dt))
      done = false;
  }
  return done;
}

void Graph::Print() const {
  for (size_t i = 0; i < edges_.size(); ++i) {
    std::cout << i << ": " << edges_[i] << "\n";
  }
}

