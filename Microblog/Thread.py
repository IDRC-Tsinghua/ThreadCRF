#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

from Node import *
from Feature import *
import numpy as np

dictLength = 137  # the length of dictionary

class Thread:
    threadCount = 0

    def __init__(self, _id, nodeList):
        assert len(nodeList) > 0
        self.id = _id
        self.nodes = nodeList
        self.nodeCount = len(self.nodes)
        self.nodeFeatures = []
        self.edgeFeatures = []
        Thread.threadCount += 1

    def setNodeFeatures(self, featureNames=[]):
        for feature in featureNames:
            self.nodeFeatures.append(newFeature(feature))

    def setEdgeFeatures(self, featureNames=[]):
        for feature in featureNames:
            self.edgeFeatures.append(newFeature(feature))

    def extractNodeFeatures(self):
        for nodeFeature in self.nodeFeatures:
            nodeFeature.extract(self.nodes)

    def extractEdgeFeatures(self):
        for edgeFeature in self.edgeFeatures:
            edgeFeature.extract(self.nodes)

    def extractFeatures(self, nodeFeatureNames=[], edgeFeatureNames=[]):
        if len(nodeFeatureNames) > 0:
            self.setNodeFeatures(nodeFeatureNames)
        if len(edgeFeatureNames) > 0:
            self.setEdgeFeatures(edgeFeatureNames)
        self.extractNodeFeatures()
        self.extractEdgeFeatures()

    def getInstance(self, addVec=False):
        n_node_features = len(self.nodeFeatures)
        n_edge_features = len(self.edgeFeatures)
        n_nodes = len(self.nodes)

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
        n_edges = n_nodes * (n_nodes - 1) / 2
        edges = np.zeros([n_edges, 2], dtype=np.int8)
        p_edge = 0
        for i in range(n_nodes):
            for j in range(i + 1, n_nodes):
                edges[p_edge] = [i, j]
                p_edge += 1

        # prepare edge_features (n_edges, n_edge_features)
        edge_features = np.zeros([n_edge_features, n_edges])
        order = 0
        for feature in self.edgeFeatures:
            tmp = np.array([feature.values[tuple(edges[i])] for i in range(n_edges)])
            edge_features[order] = tmp
            order += 1
        edge_features = np.transpose(edge_features)
        return (node_features, edges, edge_features)

    def getLabel(self):
        n_nodes = len(self.nodes)
        labels = np.zeros(n_nodes, dtype=np.int8)
        for i in range(n_nodes):
            labels[i] = self.nodes[i].label
        return labels
