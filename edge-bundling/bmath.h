#ifndef BMATH_H_
#define BMATH_H_

#include <cassert>
#include <iostream>
#include <math.h>

#define EPSILON 0.0001

class Vector;

class Point {
 public:
  Point(double x, double y) : x_(x), y_(y) { }

 private:
  friend std::ostream& operator<<(std::ostream&, const Point&);
  friend Point operator+(const Point&, const Vector&);
  friend Vector operator-(const Point&, const Point&);
  double x_, y_;
};

class Vector {
 public:
  Vector(double x, double y) : x_(x), y_(y) { }

  double dot(const Vector& b) const {
    return x_ * b.x_ + y_ * b.y_;
  }

  double length() const {
    return sqrt(dot(*this));
  }

 private:
  friend Point operator+(const Point&, const Vector&);
  friend Vector operator+(const Vector&, const Vector&);
  friend Vector operator/(const Vector&, double);
  friend Vector operator*(const Vector&, double);

  double x_, y_;
};

Vector operator+(const Vector& a, const Vector& b);
Point operator+(const Point& p, const Vector& v);
Vector operator-(const Point& z, const Point& a);
Vector operator/(const Vector& v, double d);

Vector operator*(const Vector& v, double d);
Vector operator*(double d, const Vector& v);

std::ostream& operator<<(std::ostream& os, const Point& p);

#endif  // MATH_H_
