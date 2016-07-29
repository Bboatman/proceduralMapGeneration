import unittest
from matplotlib import pyplot as plt
import json
import time
from collections import defaultdict
from EdgeBundler import EdgeBundler


class EdgeBundlerTest(unittest.TestCase):

    @staticmethod
    def drawLine(point1, point2):
        plt.plot([point1[0], point2[0]], [point1[1], point2[1]])

    def test_simpleBundling(self):
        points = [(0, 1), (0, 2), (0, 3), (0, 4), (10, 1), (10, 2), (10, 3), (10, 4)]
        adjList = [[4], [5], [6], [7], [0], [1], [2], [3]]
        numNeighbors = 2
        bundler = EdgeBundler(points, adjList, numNeighbors)
        bundler.doMingle()
        plt.clf()
        plt.axis("equal")
        # bundler.drawTree(drawLineFunc=self.drawLine)
        # plt.show()

    def test_nestedBundling(self):
        x = 20
        points = [(0, 1), (0, 2), (0, 5), (0, 6), (x, 1), (x, 2), (x, 5), (x, 6)]
        adjList = [[4], [5], [6], [7], [0], [1], [2], [3]]
        numNeighbors = 4
        bundler = EdgeBundler(points, adjList, numNeighbors)
        bundler.doMingle()
        plt.clf()
        plt.axis("equal")
        bundler.drawTree(drawLineFunc=self.drawLine)
        plt.show()

    @staticmethod
    def parseJSON(obj):
        pointDict = {}
        pointList = []
        adjDict = defaultdict(list)
        idx = 0
        for edge in obj:
            coords = edge["data"]["coords"]
            temp1 = coords[0:2]
            temp1[1] = -temp1[1]
            temp2 = coords[2:4]
            temp2[1] = -temp2[1]
            point1 = tuple(temp1)
            point2 = tuple(temp2)
            if point1 not in pointDict:
                pointDict[point1] = idx
                pointList.append(point1)
                idx += 1
            if point2 not in pointDict:
                pointDict[point2] = idx
                pointList.append(point2)
                idx += 1
            index1 = pointDict[point1]
            index2 = pointDict[point2]
            adjDict[index1].append(index2)
            adjDict[index2].append(index1)
        adjList = [adjDict[i] for i in range(len(pointList))]
        return pointList, adjList

    @staticmethod
    def showJsonData(filename):
        with open(filename) as f:
            jsonObj = json.load(f)
            points, adjList = EdgeBundlerTest.parseJSON(jsonObj)
            numNeighbors = 15
            bundler = EdgeBundler(points, adjList, numNeighbors)
            start = time.time()
            bundler.doMingle()
            print(time.time() - start)
            plt.clf()
            plt.axis("equal")
            bundler.drawTree(drawLineFunc=EdgeBundlerTest.drawLine)
            unzipped = zip(*points)
            plt.scatter(unzipped[0], unzipped[1], c="black")
            plt.show()

    def test_jsonData(self):
        self.showJsonData("testuneven.json")
        self.showJsonData("testcrossed.json")
        self.showJsonData("philippines.json")
        # self.showJsonData("eastwestcommute.json")
        # self.showJsonData("world.json")