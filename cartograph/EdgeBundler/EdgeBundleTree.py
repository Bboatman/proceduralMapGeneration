import numpy as np
from cartograph.Util import interpolate


class EdgeBundleTree:

    def __init__(self, edges):
        self.topBundles = edges
        self.newBundles = []

    @staticmethod
    def makeBundleCandidate(bundle1, bundle2):
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
        for point in combinedS:
            v = point - sCentroid
            distSum += np.dot(u, v)
            k += 1
        for point in combinedT:
            v = point - tCentroid
            distSum += -np.dot(u, v)
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
            edge1.bundle = bundle
        else:
            newBundle = Edge.parentEdge(bundleData[0], bundleData[1], bundleData[2], bundleData[3],
                                        [edge1.bundle, edge2.bundle], bundleData[4])
            edge1.bundle = newBundle
            edge2.bundle = newBundle
            self.newBundles.append(newBundle)
        edge1.bundle.grouped = True
        edge2.bundle.grouped = True

    def coalesceTree(self):
        for edge in self.newBundles:
            edge.grouped = False
            edge.mutableInkValue = np.linalg.norm(edge.tPoint - edge.sPoint)
        self.topBundles = [newBundle for newBundle in self.newBundles]
        self.newBundles = []


class Edge:
    def __init__(self, sPoint, tPoint, S, T, sCentroid, tCentroid, neighbors, children, weight, inkValue):
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
        self.grouped = False  # whether or not the edge can accept new edges into it

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
                    neighbors=neighbors, children=[], weight=1.0, inkValue=inkValue)
        return edge

    @staticmethod
    def parentEdge(sPoint, tPoint, sCentroid, tCentroid, children, inkValue):
        S = children[0].S | children[1].S
        T = children[0].T | children[1].T
        edge = Edge(np.array(sPoint), np.array(tPoint), S, T, sCentroid, tCentroid,
                    neighbors=[], children=children, weight=children[0].weight + children[1].weight, inkValue=inkValue)
        return edge

