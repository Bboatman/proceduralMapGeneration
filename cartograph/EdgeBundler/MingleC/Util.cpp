#include "Util.h"

static inline double square(double x) { return x*x;}

static Point lerp(Point& a, Point& b, double delta) {
    return Point(a.x * (1 - delta) + b.x * delta, a.y * (1 - delta) + b.y * delta);
}

static double costFunction(std::vector<Point>& S, std::vector<Point>& T, Point& sPoint, Point& tPoint) {
    double total_dist = sqrt(sPoint.sq_dist(tPoint));
    unsigned long n = S.size();
    assert(n == T.size());
    for (int i = 0; i < n; ++i) {
        const Point& xS = S[i];
        const Point& xT = T[i];
        total_dist += sqrt(sPoint.sq_dist(xS)) + sqrt(tPoint.sq_dist(xT));
    }
    return total_dist;
}



Point Point::operator-(Point &p) { return Point(x - p.x, y - p.y); }

double Point::operator*(Point &p) { return x * p.x + y * p.y; }

const double Point::sq_dist(const Point &p) {
    const double dx = x - p.x, dy = y - p.y;
    return dx * dx + dy * dy;
}
