from sklearn.neighbors import KDTree
from EdgeBundleTree import *


class EdgeBundler:

    def __init__(self, points, adjacencyList, numNeighbors):
        """
        Args:
            points: list of tuples
            adjacencyList: dictionary: pointIndex -> list of point indices of connected points
            numNeighbors: the number of edge neighbors to consider when bundling edges together
        """
        self.points = points
        self.adjacencyList = adjacencyList
        self.numNeighbors = numNeighbors
        self.edgeList = []
        self.tree = EdgeBundleTree(self._makeEdgeList())

    def _makeEdgeCoordinateList(self):
        edgeCoordinateList = []
        for i, point in enumerate(self.adjacencyList):
            point = self.points[i]
            for adjIndex in self.adjacencyList[i]:
                adjPoint = self.points[adjIndex]
                if i < adjIndex:  # only adds each pair once
                    if point[0] > adjPoint[0]:  # smaller x always goes first
                        points = (adjPoint[0], adjPoint[1], point[0], point[1])
                    else:
                        points = (point[0], point[1], adjPoint[0], adjPoint[1])
                    edgeCoordinateList.append(points)
        return edgeCoordinateList

    def _makeEdgeList(self):
        edgeCoordinateList = self._makeEdgeCoordinateList()
        self.edgeList = [Edge.leafEdge((points[0], points[1]), (points[2], points[3]), None)
                         for points in edgeCoordinateList]
        self.numNeighbors = min(self.numNeighbors, len(self.edgeList))
        tree = KDTree(edgeCoordinateList)
        for i, edgeCoordinates in enumerate(edgeCoordinateList):
            _, indices = tree.query(np.array(edgeCoordinates).reshape(1, -1), self.numNeighbors)
            self.edgeList[i].neighbors = [self.edgeList[j] for j in indices[0] if j != i]
        return self.edgeList

    def doMingle(self):
        candidateBundleList = [None for _ in range(self.numNeighbors)]
        while True:
            inkWasSaved = False
            for edge in self.edgeList:
                if not edge.bundle.grouped:
                    maxInkSaved = -float("inf")
                    maxSavingNeighborIndex = None
                    for j, neighbor in enumerate(edge.neighbors):
                        if edge.bundle == neighbor.bundle:
                            continue
                        candidateBundle = self.tree.makeBundleCandidate1(edge.bundle, neighbor.bundle)
                        candidateBundleList[j] = candidateBundle
                        inkSaved = edge.bundle.mutableInkValue + neighbor.bundle.mutableInkValue - candidateBundle[4]
                        if inkSaved > maxInkSaved:
                            maxInkSaved = inkSaved
                            maxSavingNeighborIndex = j
                    if maxInkSaved > 0:
                        self.tree.applyBundle(candidateBundleList[maxSavingNeighborIndex],
                                              edge,
                                              edge.neighbors[maxSavingNeighborIndex])
                        inkWasSaved = True
            if not inkWasSaved:
                break
            self.tree.coalesceTree()
        return self.tree

    def drawTree(self, drawLineFunc):
        def drawEdge(e):
            for child in e.children:
                drawLineFunc(e.sPoint, child.sPoint)
                drawLineFunc(e.tPoint, child.tPoint)
                drawEdge(child)

        topEdgesDict = {}
        for edge in self.tree.edges:
            topEdgesDict[edge.bundle.id] = edge.bundle
        for edgeId in topEdgesDict:
            edge = topEdgesDict[edgeId]
            drawLineFunc(edge.sPoint, edge.tPoint)
            drawEdge(edge)
