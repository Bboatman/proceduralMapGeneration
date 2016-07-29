import numpy as np
from cartograph.Utils import interpolate
from Vertex import Vertex


class NoisyEdgesMaker:
    """
    Implementation based on https://github.com/amitp/mapgen2/blob/master/NoisyEdges.as,
    but improved to account for concave quadrilaterals formed by the Voronoi vertices and the
    region points.
    """

    def __init__(self, vertices, minBorderNoiseLength):
        self.vertices = vertices
        self.minBorderNoiseLength = minBorderNoiseLength
        self.edge = []

    @staticmethod
    def perpendicular(v):
        p = np.empty_like(v)
        p[0] = -v[1]
        p[1] = v[0]
        return p

    @staticmethod
    def intersect(a0, a1, b0, b1):
        """Magical method of magic that returns intersection between lines defined by (pt0, pt1) and (pt2, pt3)
        http://www.cs.mun.ca/~rod/2500/notes/numpy-arrays/numpy-arrays.html"""
        d1 = a1 - a0
        d2 = b1 - b0
        d3 = a0 - b0
        perp = NoisyEdgesMaker.perpendicular(d1)
        denominator = np.dot(perp, d2)
        numerator = np.dot(perp, d3)
        return (numerator / denominator) * d2 + b0

    def _subdivide(self, a, b, c, d):
        """
        Subdivide the quadrilateral into smaller segments, adding the center to the edge
        """
        if np.linalg.norm(np.subtract(b, a)) < self.minBorderNoiseLength or \
                np.linalg.norm(np.subtract(c, d)) < self.minBorderNoiseLength:
            return

        # get random center point
        rand0, rand1 = np.random.uniform(0.2, 0.8, 2)
        e = interpolate(a, d, rand0)
        f = interpolate(b, c, rand0)
        g = interpolate(a, b, rand1)
        i = interpolate(d, c, rand1)

        h = interpolate(e, f, rand1)  # center

        # make new quadrilaterals and recurse
        rand2, rand3 = np.random.uniform(0.6, 1.4, 2)
        self._subdivide(a, interpolate(g, b, rand2), h, interpolate(e, d, rand3))
        self.edge.append(h)
        self._subdivide(h, interpolate(f, c, rand2), c, interpolate(i, d, rand3))

    def _makeNoisyEdge(self, pt0, pt1, pt2, pt3, processed=False):
        """
        Make a noisy edge from two Voronoi vertices (pt0 and pt2) and two region points (pt1 and pt3)
        """
        u = np.subtract(pt2, pt0)
        v = np.subtract(pt1, pt0)

        # check concavity
        if not processed:
            w = np.subtract(pt1, pt2)
            bool0 = np.dot(u, v) > 0
            bool1 = np.dot(u, w) > 0
            convex = bool0 ^ bool1
            if not convex:
                midpoint = interpolate(pt0, pt2)
                perp = self.perpendicular(u)
                pointToUse = pt0 if bool0 and bool1 else pt2  # are the region points behind the second vertex?
                perpendicularPoint = np.add(midpoint, perp)
                pt1 = self.intersect(pointToUse, pt1, midpoint, perpendicularPoint)
                pt3 = self.intersect(pointToUse, pt3, midpoint, perpendicularPoint)
                self._makeNoisyEdge(pt0, pt1, pt2, pt3, True)
                return

        # check for large or small
        dist = np.linalg.norm(u)
        u = u / dist  # numpy doesn't like augmented assignment here
        distToRegionPoint = np.linalg.norm(v - u * np.dot(u, v))
        multiplier = np.clip(distToRegionPoint,
                             min(self.minBorderNoiseLength / 10, dist * 1.61803398875),  # golden ratio, cause why not?
                             self.minBorderNoiseLength * 10)

        midpoint = interpolate(pt0, pt2)
        perp = self.perpendicular(u) * multiplier
        pt1 = midpoint + perp
        pt3 = midpoint - perp

        mid0 = interpolate(pt0, pt1)
        mid1 = interpolate(pt1, pt2)
        mid2 = interpolate(pt2, pt3)
        mid3 = interpolate(pt3, pt0)
        self._subdivide(pt0, mid0, midpoint, mid3)
        self.edge.append(midpoint)
        self._subdivide(midpoint, mid1, pt2, mid2)

    def makeNoisyEdges(self, circular):
        """
        Make a noisy edge from the list of vertices given in the constructor
        Args:
            circular: Whether or not the region is circular

        Returns:
            A new list of Vertex objects defining the new noised border. The new vertices will have index None, but
            the original information from the input vertices is preserved (i.e., new vertices are added in between
            the input ones).
        """
        if circular:
            self.vertices.append(self.vertices[0])
        noisedVertices = [self.vertices[0]]
        for i in range(len(self.vertices) - 1):
            self.edge = []
            vertex0 = self.vertices[i]
            vertex1 = self.vertices[i + 1]
            points = [np.array(point) for point in vertex0.regionPoints & vertex1.regionPoints]
            assert len(points) == 2
            self._makeNoisyEdge(np.array((vertex0.x, vertex0.y)), points[0],
                                np.array((vertex1.x, vertex1.y)), points[1])
            for j in range(1, len(self.edge) - 1):
                noisedVertices.append(Vertex(None, self.edge[j], True))
            noisedVertices.append(vertex1)
        if circular:
            noisedVertices.pop()
        return noisedVertices
