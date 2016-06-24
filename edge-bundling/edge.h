#ifndef EDGE_H_
#define EDGE_H_

#include <cstdlib>
#include <iostream>
#include <vector>

#include "bmath.h"

class Edge {
 public:
  Edge(const Point& a, const Point& z);

  void Subdivide(size_t num_segments);

  void ClearForces();

  void AddSpringForces();
  void AddElectrostaticForces(const Edge& q);

  // return true if update causes > EPSILON movement
  bool UpdatePositions(double dt);

 private:
  friend std::ostream& operator<<(std::ostream&, const Edge&);

  double Compatibility(const Edge& q) const;

  std::vector<Vector> forces_;
  std::vector<Vector> velocities_;
  std::vector<Point> points_;
};

std::ostream& operator<<(std::ostream& os, const Edge& e);

#endif  // EDGE_H_
