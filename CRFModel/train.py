#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

import sys
import pdb
from pystruct.models import EdgeFeatureGraphCRF
from pystruct.learners import OneSlackSSVM

sys.path.append("../")
from Microblog.Thread import Thread, dictLength
from Microblog.Node import Node
import json, os

data_path = '../data/weibo/'
node_features = ['NodeEmoji']
edge_features = ['SameAuthor',
                 'Similarity',
                 'SentimentProp',
                 'AuthorRef',
                 'HashTag',
                 'SameEmoji',
                 'Sibling']

if __name__ == '__main__':
    fold_names = os.listdir(data_path)
    folds = []
    for fold_name in fold_names:
        print fold_name
        X = []
        Y = []
        threads = []
        files = os.listdir(data_path + fold_name)
        for file in files:
            print file
            fin_data = open(data_path + fold_name + '/' + file, 'r')
            nodeList = []
            preID = 0
            line = fin_data.readline().strip()
            while line:
                node = Node(json.loads(line))
                if node.id != preID and preID != 0:
                    thread = Thread(preID, nodeList)
                    thread.setNodeFeatures(node_features)
                    thread.setEdgeFeatures(edge_features)
                    thread.extractFeatures()
                    threads.append(thread)
                    X.append(thread.getInstance(addVec=True))
                    Y.append(thread.getLabel())
                    nodeList = []
                nodeList.append(node)
                preID = node.id
                line = fin_data.readline().strip()
            thread = Thread(preID, nodeList)
            thread.setNodeFeatures(node_features)
            thread.setEdgeFeatures(edge_features)
            thread.extractFeatures()
            threads.append(thread)
            X.append(thread.getInstance(addVec=True))
            Y.append(thread.getLabel())
        print len(threads)
        part_threads = []
        part_X = []
        part_Y = []
        for i in range(len(threads)):
            if i % 5 > 0 and i % 5 <= 1:
                part_threads.append(threads[i])
                part_X.append(X[i])
                part_Y.append(Y[i])
        # folds.append({'threads': threads, 'X': X, 'Y': Y})
        folds.append({'threads': part_threads, 'X': part_X, 'Y': part_Y})

    crf = EdgeFeatureGraphCRF(n_states=3,
                              n_features=len(node_features) + dictLength,
                              n_edge_features=len(edge_features),
                              #class_weight=[1.3, 0.8, 1.0])
                              class_weight=[0.246, 0.394, 0.36])
    ssvm = OneSlackSSVM(crf,
                        inference_cache=100,
                        C=.1,
                        tol=.001,
                        max_iter=10000,
                        n_jobs=3)

    accuracy = 0.0
    total_correct = 0
    total = 0
    precision = {0: [0, 0], 1: [0, 0], 2: [0, 0]}
    recall = {0: [0, 0], 1: [0, 0], 2: [0, 0]}
    for fold in range(5):
        print 'fold ' + str(fold) + "--------------------------"
        X = []
        Y = []
        for i in range(5):
            if i == fold:
                continue
            X.extend(folds[i]['X'])
            Y.extend(folds[i]['Y'])
        print "Training Size: ", len(X), len(Y)
        ssvm.fit(X, Y)
        print 'Train Score: ' + str(ssvm.score(X, Y))
        # w = Weight(ssvm.w, node_features, edge_features, dictLength)

        fold_correct = 0
        fold_total = 0
        testX = folds[fold]['X']
        testY = folds[fold]['Y']
        for i in range(len(testX)):
            print "Instance: " + str(i)
            print folds[fold]['threads'][i].id
            Yi = testY[i]
            print list(Yi)
            infY = crf.inference(testX[i], ssvm.w)
            print list(infY)
            for py in range(len(Yi)):
                recall[Yi[py]][1] += 1
                if infY[py] == Yi[py]:
                    recall[Yi[py]][0] += 1
            for py in range(len(infY)):
                precision[infY[py]][1] += 1
                if infY[py] == Yi[py]:
                    precision[infY[py]][0] += 1
            fold_total += len(Yi)
            for r in range(len(Yi)):
                if Yi[r] == infY[r]:
                    fold_correct += 1
        total_correct += fold_correct
        total += fold_total
        fold_acc = float(fold_correct) / float(fold_total)
        print "fold " + str(fold) + ": " + str(fold_acc)
    print "========================================"
    print "Average Accuracy: " + str(float(total_correct) / float(total))
    print precision
    for label in precision:
        print label, float(precision[label][0]) / float(precision[label][1])
    print recall
    for label in recall:
        print label, float(recall[label][0]) / float(recall[label][1])
