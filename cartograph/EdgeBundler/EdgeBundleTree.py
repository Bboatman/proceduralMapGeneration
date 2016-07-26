import numpy as np
from cartograph.Util import interpolate
from math import sqrt
from scipy.optimize import minimize_scalar


class EdgeBundleTree:

    def __init__(self, edges):
        self.edges = edges

    @staticmethod
    def costFunction(x, sCentroid, tCentroid, S, T):
        retVal = 0
        m1 = interpolate(sCentroid, tCentroid, 1-x)
        m2 = interpolate(sCentroid, tCentroid, x)
        for point in S:
            retVal += np.linalg.norm(point - m1)
        for point in T:
            retVal += np.linalg.norm(point - m2)
        return retVal + np.linalg.norm(m1 - m2)

    @staticmethod
    def makeBundleCandidate1(bundle1, bundle2):
        sCentroid = (bundle1.weight * bundle1.sCentroid + bundle2.weight * bundle2.sCentroid) \
                    / (bundle1.weight + bundle2.weight)
        tCentroid = (bundle1.weight * bundle1.tCentroid + bundle2.weight * bundle2.tCentroid) \
                    / (bundle1.weight + bundle2.weight)
        u = tCentroid - sCentroid
        distSum = 0
        k = 0
        combinedS = bundle1.S | bundle2.S
        combinedT = bundle1.T | bundle2.T
        for point in combinedS:
            v = point - sCentroid
            distSum += np.dot(u, v)
            k += 1
        for point in combinedT:
            v = point - tCentroid
            distSum -= np.dot(u, v)
            k += 1
        d = np.linalg.norm(tCentroid - sCentroid)
        x = ((distSum + 2 * d) / (k + 4) / d)
        sPoint, tPoint = interpolate(sCentroid, tCentroid, 1 - x), interpolate(sCentroid, tCentroid, x)
        inkValueCombined = np.linalg.norm(tPoint - sPoint)
        for point in combinedS:
            inkValueCombined += np.linalg.norm(point - sPoint)
        for point in combinedT:
            inkValueCombined += np.linalg.norm(point - tPoint)
        return sPoint, tPoint, sCentroid, tCentroid, inkValueCombined

    @staticmethod
    def makeBundleCandidate2(bundle1, bundle2):
        sCentroid = (bundle1.weight * bundle1.sCentroid + bundle2.weight * bundle2.sCentroid) \
                    / (bundle1.weight + bundle2.weight)
        tCentroid = (bundle1.weight * bundle1.tCentroid + bundle2.weight * bundle2.tCentroid) \
                    / (bundle1.weight + bundle2.weight)
        u = tCentroid - sCentroid
        d = np.linalg.norm(tCentroid - sCentroid)
        u = u / np.linalg.norm(u)
        xx = []
        yy = []
        combinedS = bundle1.S | bundle2.S
        combinedT = bundle1.T | bundle2.T
        for point in combinedS:
            v = point - sCentroid
            dot = np.dot(u, v)
            xx.append(dot)
            yy.append(np.linalg.norm(v - u * dot))
        for point in combinedT:
            v = point - tCentroid
            dot = -np.dot(u, v)
            xx.append(dot)
            yy.append(np.linalg.norm(v - u * dot))
        res = minimize_scalar(EdgeBundleTree.costFunction, bracket=(0, 1),
                              args=(sCentroid, tCentroid, combinedS, combinedT),
                              bounds=(0, 1), method="Golden")
        x = res.x
        sPoint, tPoint = interpolate(sCentroid, tCentroid, 1 - x), interpolate(sCentroid, tCentroid, x)
        inkValue = EdgeBundleTree.costFunction(x, sCentroid, tCentroid, combinedS, combinedT)
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
        S = children[0].S | children[1].S
        T = children[0].T | children[1].T
        edge = Edge(np.array(sPoint), np.array(tPoint), S, T, sCentroid, tCentroid,
                    neighbors=[], children=children, weight=children[0].weight + children[1].weight,
                    inkValue=inkValue, grouped=True)
        return edge
