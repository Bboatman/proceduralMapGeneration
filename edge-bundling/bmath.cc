#include <iostream>

#include "bmath.h"

Vector operator+(const Vector& a, const Vector& b) {
  return Vector(a.x_ + b.x_, a.y_ + b.y_);
}

Point operator+(const Point& p, const Vector& v) {
  return Point(p.x_ + v.x_, p.y_ + v.y_);
}

Vector operator-(const Point& z, const Point& a) {
  return Vector(z.x_ - a.x_, z.y_ - a.y_);
}

Vector operator/(const Vector& v, double d) {
  assert(fabs(d) > EPSILON);
  return Vector(v.x_ / d, v.y_ / d);
}

Vector operator*(const Vector& v, double d) {
  return Vector(v.x_ * d, v.y_ * d);
}

Vector operator*(double d, const Vector& v) {
  return v * d;
}

std::ostream& operator<<(std::ostream& os, const Point& p) {
  return os << "(" << p.x_ << ", " << p.y_ << ")";
}

