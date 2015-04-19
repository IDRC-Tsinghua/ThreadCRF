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
edge_features = ['SameAuthor', 'Sibling', 'Similarity', 'SentimentProp', 'Difference',
                 'AuthorRef', 'HashTag', 'SameEmoji', 'FollowRoot']

if __name__ == '__main__':
    files = os.listdir(data_path)
    X = []
    Y = []
    threads = []
    for file in files:
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

    threads = threads[:100]
    X = X[:100]
    Y = Y[:100]
    accuracy = 0.0
    for fold in range(10):
        print 'fold ' + str(fold) + "--------------------------"
        ssvm.fit(X[:fold * 10] + X[(fold + 1) * 10:], Y[:fold * 10] + Y[(fold + 1) * 10:])
        print 'Train Score: ' + str(
            ssvm.score(X[:fold * 10] + X[(fold + 1) * 10:], Y[:fold * 10] + Y[(fold + 1) * 10:]))
        # w = Weight(ssvm.w, node_features, edge_features, dictLength)

        #SeqInf = SequentialInferencer(w)
        #IntInf = IntegralInferencer(w)
        correct = 0
        total = 0
        for i in range(10):
            print "Instance: " + str(fold * 10 + i)
            print list(Y[fold * 10 + i])
            #predY, potentials = SeqInf.predict(threads[fold*10+i])
            #print predY, potentials
            #print IntInf.predict(threads[i], list(Y[i]))
            infY = crf.inference(X[fold * 10 + i], ssvm.w)
            print list(infY)
            total += len(Y[fold * 10 + i])
            for r in range(len(Y[fold * 10 + i])):
                if Y[fold * 10 + i][r] == infY[r]:
                    correct += 1
        fold_acc = float(correct) / float(total)
        accuracy += fold_acc
        print "fold " + str(fold) + ": " + str(fold_acc)
    print "========================================"
    print "Average Accuracy: " + str(accuracy / 10)
