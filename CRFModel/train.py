#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

from pystruct import models
from Microblog.Thread import Thread
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

    model = models.EdgeFeatureGraphCRF()
