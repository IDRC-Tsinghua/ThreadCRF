#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

import numpy as np

from Feature import *

dictLength = 19902 + len(positiveEmoji) + len(neutralEmoji) + len(negativeEmoji)  # the length of dictionary

class Thread:
    threadCount = 0

    def __init__(self, _id, nodeList, cliqueSize=3):
        assert len(nodeList) > 0
        self.id = _id
        self.nodes = nodeList
        self.nodeCount = len(self.nodes)
        n_edges = 0
        for node in nodeList:
            n_edges += min(cliqueSize - 1, node.depth)
            for ci in range(len(node.children)):
                for cj in range(ci + 1, len(node.children)):
                    if node.children[ci] >= len(nodeList) or node.children[cj] >= len(nodeList):
                        continue
                    n_edges += 1
        self.edgeCount = n_edges
        self.nodeFeatureNames = []
        self.edgeFeatureNames = []
        self.nodeFeatures = []
        self.edgeFeatures = []
        self.cliqueSize = cliqueSize  # number of nodes in a clique
        Thread.threadCount += 1

    def setNodeFeatures(self, featureNames=[]):
        self.nodeFeatureNames = featureNames
        for feature in featureNames:
            self.nodeFeatures.append(newFeature(feature))

    def setEdgeFeatures(self, featureNames=[]):
        self.edgeFeatureNames = featureNames
        for feature in featureNames:
            self.edgeFeatures.append(newFeature(feature))

    def extractNodeFeatures(self):
        for nodeFeature in self.nodeFeatures:
            nodeFeature.extract(self.nodes, self.cliqueSize)

    def extractEdgeFeatures(self):
        for edgeFeature in self.edgeFeatures:
            edgeFeature.extract(self.nodes, self.cliqueSize)

    def extractFeatures(self, nodeFeatureNames=[], edgeFeatureNames=[]):
        if len(nodeFeatureNames) > 0:
            self.setNodeFeatures(nodeFeatureNames)
        if len(edgeFeatureNames) > 0:
            self.setEdgeFeatures(edgeFeatureNames)
        self.extractNodeFeatures()
        self.extractEdgeFeatures()

    def getInstance(self, addVec=False, addEdgeFeature=True):
        n_node_features = len(self.nodeFeatures)
        n_edge_features = len(self.edgeFeatures)
        n_nodes = self.nodeCount
        n_edges = self.edgeCount

        # prepare node_features (n_nodes, n_node_features)
        if addVec:
            node_features = np.zeros([n_node_features + dictLength, n_nodes])
        else:
            node_features = np.zeros([n_node_features, n_nodes])
        order = 0
        for feature in self.nodeFeatures:
            tmp = np.array([feature.values[i] for i in range(n_nodes)])
            node_features[order] = tmp
            order += 1
        node_features = np.transpose(node_features)
        if addVec:
            for i in range(n_nodes):
                node_features[i][-dictLength:] = self.nodes[i].toVector(dictLength)

        # prepare edges (n_edges, 2)
        edges = []
        for i in range(1, len(self.nodes)):
            ancestors = []
            tmp = self.nodes[i].parent
            for ans in range(1, self.cliqueSize):
                ancestors.append(tmp)
                tmp = self.nodes[tmp].parent
                if tmp == -1:
                    break
            for j in ancestors:
                edges.append([j, i])
        for i in range(0, len(self.nodes)):
            chdnList = self.nodes[i].children
            if len(chdnList) > 1:
                for ci in range(len(chdnList)):
                    for cj in range(ci + 1, len(chdnList)):
                        if chdnList[ci] >= len(self.nodes) or chdnList[cj] >= len(self.nodes):
                            continue
                        edges.append([ci, cj])
        assert len(edges) == n_edges
        edges = np.array(edges)

        # prepare edge_features (n_edges, n_edge_features)
        edge_features = np.zeros([n_edge_features, n_edges])
        order = 0
        for feature in self.edgeFeatures:
            tmp = [0] * n_edges
            for i in range(n_edges):
                if tuple(edges[i]) in feature.values:
                    tmp[i] = feature.values[tuple(edges[i])]
                else:
                    tmp[i] = 0

            edge_features[order] = np.array(tmp, dtype=np.int8)
            order += 1
        edge_features = np.transpose(edge_features)
        return (node_features, edges, edge_features)

    def getLabel(self):
        n_nodes = len(self.nodes)
        labels = np.zeros(n_nodes, dtype=np.int8)
        for i in range(n_nodes):
            labels[i] = self.nodes[i].label
        return labels
