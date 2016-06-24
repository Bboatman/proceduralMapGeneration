#include "edge.h"

#define K (0.01)

Edge::Edge(const Point& a, const Point& z) : points_(2, Point(0, 0)) {
  points_[0] = a;
  points_[1] = z;
}

void Edge::Subdivide(size_t num_segments) {
  const Vector delta = points_[1] - points_[0];
  const Vector subdelta = delta / num_segments;

  points_.resize(num_segments + 1, Point(0, 0));
  points_[num_segments] = points_[1];
  for (size_t i = 0; i < num_segments; ++i) {
    points_[i] = points_[0] + (i * subdelta);
  }

  forces_.resize(points_.size(), Vector(0, 0));
  velocities_.resize(points_.size(), Vector(0, 0));
}

void Edge::ClearForces() {
  std::fill(forces_.begin(), forces_.end(), Vector(0, 0));
}

void Edge::AddSpringForces() {
  for (size_t i = 1; i < points_.size() - 1; ++i) {
    // spring forces along edge
    Vector delta0 = points_[i-1] - points_[i];
    Vector delta1 = points_[i] - points_[i+1];

    const double delta0_len = delta0.length();
    const double delta1_len = delta1.length();

    const Vector delta0_dir = delta0 / delta0_len;
    const Vector delta1_dir = delta1 / delta1_len;

    const Vector Fs0 = delta0_dir * (K * delta0_len);
    const Vector Fs1 = delta1_dir * (K * delta1_len);

    forces_[i] = forces_[i] + Fs0 + Fs1;
  }
}

void Edge::AddElectrostaticForces(const Edge& q) {
  const double compat = Compatibility(q);

  for (size_t i = 1; i < points_.size() - 1; ++i) {
    // forces between edges
    Vector delta_e = points_[i] - q.points_[i];
    const double delta_e_len = delta_e.length();
    assert(fabs(delta_e_len) > EPSILON);
    const Vector delta_e_dir = delta_e / delta_e_len;
    const Vector Fe = delta_e_dir * (1.0 / delta_e_len);

    forces_[i] = forces_[i] + (compat * Fe);
  }
}

// return true if update causes > EPSILON movement
bool Edge::UpdatePositions(double dt) {
  bool moved = false;
  for (size_t i = 0; i < points_.size(); ++i) {
    // assumes mass == 1
    // TODO: verlet, not euler
    velocities_[i] = velocities_[i] + (forces_[i] * dt);

    const Vector delta_p = velocities_[i] * dt;
    points_[i] = points_[i] + delta_p;

    if (delta_p.length() > EPSILON)
      moved = true;
  }
  return moved;
}

double Edge::Compatibility(const Edge& q) const {
  const Vector delta_p = points_[points_.size() - 1] - points_[0];
  const Vector delta_q = q.points_[points_.size() - 1] - q.points_[0];

  const double len_p = delta_p.length();
  const double len_q = delta_q.length();

  // angle compatibility
  const double Ca = fabs(delta_p.dot(delta_q) / (len_p * len_q));

  // scale compatibility
  const double len_avg = (delta_p.length() + delta_q.length()) / 2;

  assert(len_avg > EPSILON);
  const double Cs = 2.0 /
      (len_avg * std::min(len_p, len_q) + std::max(len_p, len_q) / len_avg);

  // position compatibility
  const Point& mid_p = points_[points_.size() / 2];
  const Point& mid_q = q.points_[q.points_.size() / 2];
  const double Cp = len_avg / (len_avg + (mid_p - mid_q).length());

  // visibility compatibility
  // TODO
  const double Cv = 1.0; 

  return Ca*Cs*Cp*Cv;
}


std::ostream& operator<<(std::ostream& os, const Edge& e) {
  os << e.points_[0];
  for (size_t i = 1; i < e.points_.size(); ++i) {
    os << " -> " << e.points_[i];
  }
  return os;
}
