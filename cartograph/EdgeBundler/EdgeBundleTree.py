import numpy as np
from cartograph.Util import interpolate
from math import sqrt, tan, pi, acos


class EdgeBundleTree:

    gr = (1 + sqrt(5)) / 2
    maxTurningAngle = 180 - 45
    maxTurningAngleCot = 1 / tan(maxTurningAngle * pi / 180)

    def __init__(self, edges):
        self.edges = edges

    @staticmethod
    def goldenSectionSearch(f, a, b, tol=1e-3):
        c = b - (b - a) / EdgeBundleTree.gr
        d = a + (b - a) / EdgeBundleTree.gr
        while abs(c - d) > tol:
            if f(c) < f(d):
                b = d
            else:
                a = c
            c = b - (b - a) / EdgeBundleTree.gr
            d = a + (b - a) / EdgeBundleTree.gr
        return (b + a) / 2

    @staticmethod
    def makeBundleCandidate1(bundle1, bundle2):
        sCentroid = (bundle1.weight * bundle1.sCentroid + bundle2.weight * bundle2.sCentroid) \
                    / (bundle1.weight + bundle2.weight)
        tCentroid = (bundle1.weight * bundle1.tCentroid + bundle2.weight * bundle2.tCentroid) \
                    / (bundle1.weight + bundle2.weight)
        u = tCentroid - sCentroid
        u = u / np.linalg.norm(u)
        distSum = 0
        k = 0
        combinedS = bundle1.S | bundle2.S
        combinedT = bundle1.T | bundle2.T
        maxDist = 0
        for point in combinedS:
            v = point - sCentroid
            dist = np.dot(u, v)
            maxDist = max(maxDist, dist)
            distSum += dist
            k += 1
        for point in combinedT:
            v = point - tCentroid
            dist = -np.dot(u, v)
            maxDist = max(maxDist, dist)
            distSum += dist
            k += 1
        totalWeight = 1
        dx = tCentroid[0] - sCentroid[0]
        dy = tCentroid[1] - sCentroid[1]
        d = sqrt(dx * dx + dy * dy)
        x = ((distSum + 2 * totalWeight * d) / (k + 4 * totalWeight) / d)
        sPoint, tPoint = interpolate(sCentroid, tCentroid, 1 - x), interpolate(sCentroid, tCentroid, x)
        dx = tPoint[0] - sPoint[0]
        dy = tPoint[1] - sPoint[1]
        inkValueCombined = sqrt(dx * dx + dy * dy)
        for point in combinedS:
            dx = point[0] - sPoint[0]
            dy = point[1] - sPoint[1]
            inkValueCombined += sqrt(dx * dx + dy * dy)
        for point in combinedT:
            dx = point[0] - tPoint[0]
            dy = point[1] - tPoint[1]
            inkValueCombined += sqrt(dx * dx + dy * dy)
        return sPoint, tPoint, sCentroid, tCentroid, inkValueCombined

    @staticmethod
    def makeBundleCandidate2(bundle1, bundle2):
        sCentroid = (bundle1.weight * bundle1.sCentroid + bundle2.weight * bundle2.sCentroid) \
                    / (bundle1.weight + bundle2.weight)
        tCentroid = (bundle1.weight * bundle1.tCentroid + bundle2.weight * bundle2.tCentroid) \
                    / (bundle1.weight + bundle2.weight)
        totalWeight = 1  # (bundle1.weight + bundle2.weight) / 4.0
        combinedS = bundle1.S | bundle2.S
        combinedT = bundle1.T | bundle2.T

        u = tCentroid - sCentroid
        length = np.linalg.norm(u)
        u = u / length

        def getMaxCotVal(val):
            # This method doesn't always produce the results that one would expect. It does force angles to be at least
            # a certain value, but it doesn't take the children of edges about to be bundled into account. Individual
            # bundles are formed from points with the correct angles, but when a higher-order bundle is formed from
            # those last two, the bundling does not take the angle of child edge to edge to new bundled edge into
            # account. With proper rending, this shouldn't be much of a problem though.
            m1 = interpolate(sCentroid, tCentroid, 1 - val)
            m2 = interpolate(sCentroid, tCentroid, val)
            maxCot = -float("inf")
            maxCotHeight = -float("inf")
            for point in combinedS:
                v = point - m1
                dist = np.dot(u, v)
                heightVec = v - u * dist
                height = sqrt(heightVec[0] * heightVec[0] + heightVec[1] * heightVec[1])
                cotVal = dist / height
                if cotVal > maxCot:
                    maxCot = cotVal
                    maxCotHeight = height
            for point in combinedT:
                v = point - m2
                dist = np.dot(u, v)
                heightVec = v - u * dist
                height = sqrt(heightVec[0] * heightVec[0] + heightVec[1] * heightVec[1])
                cotVal = -dist / height
                if cotVal > maxCot:
                    maxCot = cotVal
                    maxCotHeight = height
            return maxCot, maxCotHeight

        def costFunction(val):
            assert val <= 1 or val >= 0
            retVal = 0
            m1 = interpolate(sCentroid, tCentroid, 1 - val)
            m2 = interpolate(sCentroid, tCentroid, val)
            for p in combinedS:
                dx = p[0] - m1[0]
                dy = p[1] - m1[1]
                retVal += sqrt(dx * dx + dy * dy)
            for p in combinedT:
                dx = p[0] - m2[0]
                dy = p[1] - m2[1]
                retVal += sqrt(dx * dx + dy * dy)
            dx = m2[0] - m1[0]
            dy = m2[1] - m1[1]

            totalInkVal = retVal + sqrt(dx * dx + dy * dy) * totalWeight
            return totalInkVal  # * (1 + cos(atan(getMaxTanVal(val)[0])) / 1.2)

        x = EdgeBundleTree.goldenSectionSearch(costFunction, 0, 0.5)
        maxCotVal, maxCotValValHeight = getMaxCotVal(x)
        if maxCotVal > EdgeBundleTree.maxTurningAngleCot:
            x += (maxCotVal - EdgeBundleTree.maxTurningAngleCot) * maxCotValValHeight / length
            if x > 0.5:
                return None, None, None, None, float("inf")
        sPoint, tPoint = interpolate(sCentroid, tCentroid, 1 - x), interpolate(sCentroid, tCentroid, x)
        assert sPoint[0] < tPoint[0]
        assert sPoint[0] < tPoint[0]
        inkValue = costFunction(x)
        return sPoint, tPoint, sCentroid, tCentroid, inkValue

    def applyBundle(self, bundleData, edge1, edge2):
        if edge2.bundle.grouped:
            # bundle2 should absorb bundle1
            bundle = edge2.bundle
            bundle.sPoint = bundleData[0]
            bundle.tPoint = bundleData[1]
            bundle.S.add(tuple(edge1.bundle.sPoint))
            bundle.T.add(tuple(edge1.bundle.tPoint))
            bundle.sCentroid = bundleData[2]
            bundle.tCentroid = bundleData[3]
            bundle.children.append(edge1.bundle)
            bundle.weight += edge1.bundle.weight
            bundle.mutableInkValue = bundleData[4]
            self._setBundle(edge1, bundle)
        else:
            newBundle = Edge.parentEdge(bundleData[0], bundleData[1], bundleData[2], bundleData[3],
                                        [edge1.bundle, edge2.bundle], bundleData[4])
            self._setBundle(newBundle, newBundle)

    def _setBundle(self, edge, newBundle):
        edge.bundle = newBundle
        for child in edge.children:
            self._setBundle(child, newBundle)

    def coalesceTree(self):
        for edge in self.edges:
            edge.bundle.grouped = False
            edge.bundle.mutableInkValue = np.linalg.norm(edge.bundle.tPoint - edge.bundle.sPoint)


class Edge:
    id = 0

    def __init__(self, sPoint, tPoint, S, T, sCentroid, tCentroid, neighbors, children, weight, inkValue, grouped):
        self.id = Edge.id
        Edge.id += 1
        self.sPoint = sPoint
        self.tPoint = tPoint
        self.S = S
        self.T = T
        self.sCentroid = sCentroid
        self.tCentroid = tCentroid
        self.neighbors = neighbors
        self.children = children
        self.weight = weight
        self.mutableInkValue = inkValue

        self.bundle = self
        self.grouped = grouped  # whether or not the edge can accept new edges into it

    @staticmethod
    def leafEdge(sPoint, tPoint, neighbors):
        S = set()
        T = set()
        S.add(sPoint)
        T.add(tPoint)
        sPoint = np.array(sPoint)
        tPoint = np.array(tPoint)
        inkValue = np.linalg.norm(tPoint - sPoint)
        edge = Edge(sPoint, tPoint, S, T, sPoint, tPoint,
                    neighbors=neighbors, children=[], weight=1.0, inkValue=inkValue, grouped=False)
        return edge

    @staticmethod
    def parentEdge(sPoint, tPoint, sCentroid, tCentroid, children, inkValue):
        S = set()
        T = set()
        S.add(tuple(children[0].sPoint))
        S.add(tuple(children[1].sPoint))
        T.add(tuple(children[0].tPoint))
        T.add(tuple(children[1].tPoint))
        edge = Edge(np.array(sPoint), np.array(tPoint), S, T, sCentroid, tCentroid,
                    neighbors=[], children=children, weight=children[0].weight + children[1].weight,
                    inkValue=inkValue, grouped=True)
        return edge
