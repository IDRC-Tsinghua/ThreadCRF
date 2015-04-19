#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

from Inferencer import Inferencer
from Microblog.Thread import Thread


class SequentialInferencer(Inferencer):
    "predict labels of a thread sequentially from root to leaves"

    def __init__(self, weight):
        Inferencer.__init__(self, weight)
        self.name = "SequentialInferencer"

    def predict(self, thread):
        assert thread.nodeCount > 0
        y = [-1] * thread.nodeCount
        energy = 0
        root = thread.nodes[0]
        # y[0] = root.label

        for i in range(0, thread.nodeCount):
            partThread = Thread(root.id, thread.nodes[:i + 1])
            partThread.setNodeFeatures(thread.nodeFeatureNames)
            if i != 0:
                partThread.setEdgeFeatures(thread.edgeFeatureNames)
            record = {}
            for cur_y in range(0, 3):
                y[i] = cur_y
                potentials = self.computePotentials(partThread, y[:i + 1])
                record[potentials] = cur_y
            y[i] = record[max(record.keys())]
            energy = max(record.keys())

        return y, energy