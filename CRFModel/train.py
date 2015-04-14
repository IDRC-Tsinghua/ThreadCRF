#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

from pystruct.models import EdgeFeatureGraphCRF
from pystruct.learners import OneSlackSSVM
from Microblog.Thread import Thread, dictLength
from Microblog.Node import Node
import json


if __name__ == '__main__':
    fin_data = open('../sample.txt', 'r')
    nodeList = []
    line = fin_data.readline().strip()
    root = Node(json.loads(line))
    nodeList.append(root)
    line = fin_data.readline().strip()
    while line:
        node = Node(json.loads(line))
        nodeList.append(node)
        line = fin_data.readline().strip()
    thread = Thread(root.id, nodeList)
    thread.setNodeFeatures(['Root', 'Parent', 'ParentSim', 'ParentDiff', 'SelfRepost', 'NodeEmoji'])
    thread.setEdgeFeatures(
        ['SameAuthor', 'Sibling', 'Similarity', 'SentimentProp', 'AuthorRef', 'HashTag', 'SameEmoji'])
    thread.extractFeatures()
    for nodeFeature in thread.nodeFeatures:
        print nodeFeature.name, nodeFeature.values
    for edgeFeature in thread.edgeFeatures:
        print edgeFeature.name, edgeFeature.values

    X = thread.getInstance()
    Y = thread.getLabel()
    crf = EdgeFeatureGraphCRF(n_states=3, n_features=len(thread.nodeFeatures) + dictLength,
                              n_edge_features=len(thread.edgeFeatures))
    ssvm = OneSlackSSVM(crf, inference_cache=50, C=.1, tol=.1, max_iter=1000, n_jobs=1)
    ssvm.fit([X], [Y])
    print [Y]
    print ssvm.predict([X])
    print ssvm.w
