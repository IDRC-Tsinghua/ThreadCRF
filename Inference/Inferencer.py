#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'


class Inferencer:
    "the basic class of inferencer"

    def __init__(self, weight):
        self.name = "Inferencer"
        self.w = weight

    def predict(self, thread):
        return None

    def computePotentials(self, thread, y):
        sum = 0.0
        n_nodes = len(thread.nodes)
        assert n_nodes == len(y)

        for i in range(len(y)):
            thread.nodes[i].label = y[i]
        thread.extractFeatures()

        for feature in thread.nodeFeatures:
            for node in thread.nodes:
                sum += feature.values[node.number] * self.w.w_node[feature][node.label]

        for node in thread.nodes:
            for i in node.vector:
                sum += node.vector[i] * self.w.w_dict[i][node.label]

        for i in range(0, n_nodes):
            for j in range(i + 1, n_nodes):
                for feature in thread.edgeFeatures:
                    sum += feature.values[(i, j)] * self.w.w_edge[feature][(y[i], y[j])]

        return sum