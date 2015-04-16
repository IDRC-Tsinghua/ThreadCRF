#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

from pystruct.models import EdgeFeatureGraphCRF
from pystruct.learners import OneSlackSSVM
from Microblog.Thread import Thread, dictLength
from Microblog.Node import Node
from Weights import Weight
from Inference.SequentialInferencer import SequentialInferencer
from Inference.IntegralInferencer import IntegralInferencer
import json, os

data_path = '../data/res/'
node_features = ['NodeEmoji']
edge_features = ['SameAuthor', 'Sibling', 'Similarity', 'SentimentProp',
                 'AuthorRef', 'HashTag', 'SameEmoji', 'FollowRoot']

if __name__ == '__main__':
    files = os.listdir(data_path)
    X = []
    Y = []
    threads = []
    for file in files[0:10]:
        print file
        fin_data = open(data_path + file, 'r')
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
        thread.setNodeFeatures(node_features)
        thread.setEdgeFeatures(edge_features)
        thread.extractFeatures()

        for nodeFeature in thread.nodeFeatures:
            print nodeFeature.name, nodeFeature.values
            # for edgeFeature in thread.edgeFeatures:
            #print edgeFeature.name, edgeFeature.values

        threads.append(thread)
        X.append(thread.getInstance(addVec=True))
        Y.append(thread.getLabel())

    crf = EdgeFeatureGraphCRF(n_states=3, n_features=len(node_features) + dictLength,
                              n_edge_features=len(edge_features))
    ssvm = OneSlackSSVM(crf, inference_cache=50, C=.1, tol=.1, max_iter=1000, n_jobs=1)
    ssvm.fit(X, Y)
    w = Weight(ssvm.w, node_features, edge_features, dictLength)
    print w.w_node
    print w.w_dict
    print w.w_edge

    SeqInf = SequentialInferencer(w)
    IntInf = IntegralInferencer(w)
    for i in range(len(Y)):
        print list(Y[i])
        print SeqInf.predict(threads[i])
        # print IntInf.predict(threads[i], list(Y[i]))
        print list(crf.inference(X[i], ssvm.w))
        print "--------------------------------------"
