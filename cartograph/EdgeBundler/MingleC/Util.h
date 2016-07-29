#ifndef MINGLEC_POINT_H
#define MINGLEC_POINT_H

#include <cmath>
#include <vector>
#include <cassert>

static const double PHI = (1 + sqrt(5)) / 2;
static const int UNGROUPED = -1;

struct Point {
    double x, y;
    int id;
    Point(double x, double y) : x(x), y(y) {}

    Point operator- (Point& p);
    double operator* (Point& p);
    const double sq_dist(const Point& p);
};


static inline double square(double x);
static Point lerp(Point& a, Point& b, double delta);
static double costFunction(std::vector<Point>& S, std::vector<Point>& T, Point& sPoint, Point& tPoint);


#endif //MINGLEC_POINT_H
