#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

import math

from Emoji import *


class Feature:
    def __init__(self):
        self.name = "Feature"
        self.values = {}
        self.sim_threshold = 0.1  # to be tuned
        self.diff_threshold = 0  # to be tuned
        # print "Feature initialized"

    def cosineSim(self, A, B, BOW=True):
        sum_AB = 0.0
        sum_A2 = 0.0
        sum_B2 = 0.0
        if BOW:
            for i in list(set(A.keys()) & set(B.keys())):
                sum_AB += A[i] * B[i]
            for i in A:
                sum_A2 += A[i] ** 2
            for i in B:
                sum_B2 += B[i] ** 2
        else:
            assert len(A) == len(B)
            for i in range(len(A)):
                sum_AB += A[i] * B[i]
                sum_A2 += A[i] ** 2
                sum_B2 += B[i] ** 2
        sum_A2 = max(1.0, sum_A2)
        sum_B2 = max(1.0, sum_B2)
        return sum_AB / (math.sqrt(sum_A2) * math.sqrt(sum_B2))

    def distance(self, i, j, nodeList):
        curNode = nodeList[i]
        depth = 0
        i_ancestor = {}
        while curNode.number != 0:
            i_ancestor[curNode.number] = depth
            curNode = nodeList[curNode.parent]
            depth += 1
        i_ancestor[0] = depth

        curNode = nodeList[j]
        depth = 0
        while not curNode.number in i_ancestor:
            curNode = nodeList[curNode.parent]
            depth += 1

        return depth + i_ancestor[curNode.number]

    def isAncestor(self, j, i, nodeList):
        "decide whether j is i's ancestor in the nodelist"
        curNode = nodeList[i]
        depth = 1
        while curNode.number != 0:
            if curNode.parent == j:
                return True, depth
            else:
                curNode = nodeList[curNode.parent]
                depth += 1
        if j == 0:
            return True, depth
        else:
            return False, -1

    def extract(self, nodeList, clique_size):
        return

        # def __del__(self):
        # print "Feature destroyed"


class NodeFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "NodeFeature"
        # print "NodeFeature initialized"

        # def __del__(self):
        #print "NodeFeature destroyed"


class EdgeFeature(Feature):
    def __init__(self):
        Feature.__init__(self)
        self.name = "EdgeFeature"
        # print "EdgeFeature initialized"

        # def __del__(self):
        #print "EdgeFeature destroyed"


class Root(NodeFeature):
    "test whether this node has the same label as root"

    def __init__(self):
        NodeFeature.__init__(self)
        self.name = "Root"
        # print "NodeFeature Root(yi) initialized"

    def extract(self, nodeList):
        assert len(nodeList) > 0
        root = nodeList[0]
        self.values[root.number] = 1
        if len(nodeList) == 1:
            return
        for node in nodeList[1:]:
            if node.label == root.label:
                self.values[node.number] = 1
            else:
                self.values[node.number] = 0


class Parent(NodeFeature):
    "test whether this node has the same label as its parent"

    def __init__(self):
        NodeFeature.__init__(self)
        self.name = "Parent"
        # print "NodeFeature Parent(yi) initialized"

    def extract(self, nodeList):
        assert len(nodeList) > 0
        root = nodeList[0]
        self.values[root.number] = 0
        if len(nodeList) == 1:
            return
        for node in nodeList[1:]:
            if node.label == nodeList[node.parent].label:
                self.values[node.number] = 1
            else:
                self.values[node.number] = 0


class ParentSim(NodeFeature):
    "test whether this node and its parent have similar text and the same label"

    def __init__(self):
        NodeFeature.__init__(self)
        self.name = "ParentSim"
        # print "NodeFeature ParentSim(yi) initialized"

    def extract(self, nodeList):
        assert len(nodeList) > 0
        root = nodeList[0]
        self.values[root.number] = 0
        if len(nodeList) == 1:
            return
        for node in nodeList[1:]:
            if self.cosineSim(node.vector, nodeList[node.parent].vector) >= self.sim_threshold \
                    and node.label == nodeList[node.parent].label:
                self.values[node.number] = 1
            else:
                self.values[node.number] = 0


class ParentDiff(NodeFeature):
    "test whether this node and its parent have very different text and different label"

    def __init__(self):
        NodeFeature.__init__(self)
        self.name = "ParentDiff"
        # print "NodeFeature ParentDiff(yi) initialized"

    def extract(self, nodeList):
        assert len(nodeList) > 0
        root = nodeList[0]
        self.values[root.number] = 0
        if len(nodeList) == 1:
            return
        for node in nodeList[1:]:
            if self.cosineSim(node.vector, nodeList[node.parent].vector) < self.sim_threshold \
                    and node.label != nodeList[node.parent].label:
                self.values[node.number] = 1
            else:
                self.values[node.number] = 0


class SelfRepost(NodeFeature):
    "test whether this node and its parent are by the same author and have the same label"

    def __init__(self):
        NodeFeature.__init__(self)
        self.name = "SelfRepost"
        # print "NodeFeature SelfRepost(yi) initialized"

    def extract(self, nodeList):
        assert len(nodeList) > 0
        root = nodeList[0]
        self.values[root.number] = 0
        if len(nodeList) == 1:
            return
        for node in nodeList[1:]:
            if node.name == nodeList[node.parent].name \
                    and node.label == nodeList[node.parent].label:
                self.values[node.number] = 1
            else:
                self.values[node.number] = 0


class NodeEmoji(NodeFeature):

    def __init__(self):
        NodeFeature.__init__(self)
        self.name = "NodeEmoji"
        # print "NodeFeature NodeEmoji initialized"

    def extract(self, nodeList, clique_size):
        assert len(nodeList) > 0
        for node in nodeList:
            self.values[node.number] = 0
            if node.emoji:
                allEmoji = set(node.emoji)
                labelSum = 0
                for emoji in allEmoji:
                    labelSum += getEmojiLabel(emoji)
                '''if labelSum == 0:
                    emojiLabel = 0
                elif labelSum > 0:
                    emojiLabel = 1
                else:
                    emojiLabel = -1'''
                self.values[node.number] = labelSum


class SameAuthor(EdgeFeature):

    def __init__(self):
        EdgeFeature.__init__(self)
        self.name = "SameAuthor"
        # print "EdgeFeature SameAuthor initialized"

    def extract(self, nodeList, clique_size):
        assert len(nodeList) > 1
        for i in range(1, len(nodeList)):
            ancestors = []
            tmp = nodeList[i].parent
            for ans in range(1, clique_size):
                ancestors.append(tmp)
                tmp = nodeList[tmp].parent
                if tmp == -1:
                    break
            for j in ancestors:
                if nodeList[i].name == nodeList[j].name:
                    self.values[(j, i)] = 1
                else:
                    self.values[(j, i)] = 0
        for i in range(0, len(nodeList)):
            chdnList = nodeList[i].children
            if len(chdnList) <= 1:
                continue
            for ci in range(len(chdnList)):
                for cj in range(ci + 1, len(chdnList)):
                    if chdnList[ci] >= len(nodeList) or chdnList[cj] >= len(nodeList):
                        continue
                    if nodeList[chdnList[ci]].name == nodeList[chdnList[cj]].name:
                        self.values[(chdnList[ci], chdnList[cj])] = 1
                    else:
                        self.values[(chdnList[ci], chdnList[cj])] = 0


class Sibling(EdgeFeature):

    def __init__(self):
        EdgeFeature.__init__(self)
        self.name = "Sibling"
        # print "EdgeFeature Sibling initialized"

    def extract(self, nodeList, clique_size):
        assert len(nodeList) > 1
        for i in range(0, len(nodeList)):
            chdnList = nodeList[i].children
            if len(chdnList) <= 1:
                continue
            for ci in range(len(chdnList)):
                for cj in range(ci + 1, len(chdnList)):
                    if chdnList[ci] >= len(nodeList) or chdnList[cj] >= len(nodeList):
                        continue
                    if self.cosineSim(nodeList[chdnList[ci]].vector,
                                      nodeList[chdnList[cj]].vector) >= self.sim_threshold \
                            or len(set(nodeList[chdnList[ci]].hashtag) & set(nodeList[chdnList[cj]].hashtag)) > 0 \
                            or len(set(nodeList[chdnList[ci]].emoji) & set(nodeList[chdnList[cj]].emoji)) > 0 \
                            or nodeList[chdnList[ci]].name == nodeList[chdnList[cj]].name:
                        self.values[(chdnList[ci], chdnList[cj])] = 1
                    else:
                        self.values[(chdnList[ci], chdnList[cj])] = 0


class Similarity(EdgeFeature):
    "test whether two nodes have similar text"

    def __init__(self):
        EdgeFeature.__init__(self)
        self.name = "Similarity"
        # print "EdgeFeature Similarity initialized"

    def extract(self, nodeList, clique_size):
        assert len(nodeList) > 1
        for i in range(1, len(nodeList)):
            ancestors = []
            tmp = nodeList[i].parent
            for ans in range(1, clique_size):
                ancestors.append(tmp)
                tmp = nodeList[tmp].parent
                if tmp == -1:
                    break
            for j in ancestors:
                if self.cosineSim(nodeList[i].vector, nodeList[j].vector) >= self.sim_threshold:
                    self.values[(j, i)] = math.exp(1 - self.distance(i, j, nodeList))
                else:
                    self.values[(j, i)] = 0
        for i in range(0, len(nodeList)):
            chdnList = nodeList[i].children
            if len(chdnList) <= 1:
                continue
            for ci in range(len(chdnList)):
                for cj in range(ci + 1, len(chdnList)):
                    if chdnList[ci] >= len(nodeList) or chdnList[cj] >= len(nodeList):
                        continue
                    if self.cosineSim(nodeList[chdnList[ci]].vector,
                                      nodeList[chdnList[cj]].vector) >= self.sim_threshold:
                        self.values[(chdnList[ci], chdnList[cj])] = 1
                    else:
                        self.values[(chdnList[ci], chdnList[cj])] = 0


class Difference(EdgeFeature):
    "test whether two nodes have different text"

    def __init__(self):
        EdgeFeature.__init__(self)
        self.name = "Difference"
        # print "EdgeFeature Difference initialized"

    def extract(self, nodeList, clique_size):
        assert len(nodeList) > 1
        for i in range(1, len(nodeList)):
            ancestors = []
            tmp = nodeList[i].parent
            for ans in range(1, clique_size):
                ancestors.append(tmp)
                tmp = nodeList[tmp].parent
                if tmp == -1:
                    break
            for j in ancestors:
                if self.cosineSim(nodeList[i].vector, nodeList[j].vector) <= self.diff_threshold:
                    self.values[(j, i)] = -math.exp(1 - self.distance(i, j, nodeList))
                else:
                    self.values[(j, i)] = 0


class SentimentProp(EdgeFeature):
    "test the sentiment propagation relation in routes"

    def __init__(self):
        EdgeFeature.__init__(self)
        self.name = "SentimentProp"
        # print "EdgeFeature SentimentProp initialized"

    def extract(self, nodeList, clique_size):
        assert len(nodeList) > 1
        for i in range(1, len(nodeList)):
            ancestors = []
            tmp = nodeList[i].parent
            for ans in range(1, clique_size):
                ancestors.append(tmp)
                tmp = nodeList[tmp].parent
                if tmp == -1:
                    break
            for j in ancestors:
                isAnc, distance = self.isAncestor(j, i, nodeList)
                if isAnc:
                    self.values[(j, i)] = math.exp(1 - distance)
                else:
                    self.values[(j, i)] = 0


class AuthorRef(EdgeFeature):
    "test whether the node's author is mentioned by its ancestor"

    def __init__(self):
        EdgeFeature.__init__(self)
        self.name = "AuthorRef"
        # print "EdgeFeature AuthorRef initialized"

    def extract(self, nodeList, clique_size):
        assert len(nodeList) > 1
        for i in range(1, len(nodeList)):
            ancestors = []
            tmp = nodeList[i].parent
            for ans in range(1, clique_size):
                ancestors.append(tmp)
                tmp = nodeList[tmp].parent
                if tmp == -1:
                    break
            for j in ancestors:
                if nodeList[i].name in nodeList[j].mention:
                    self.values[(j, i)] = 1
                else:
                    self.values[(j, i)] = 0


class HashTag(EdgeFeature):
    "test whether two nodes have the same hashtag and label"

    def __init__(self):
        EdgeFeature.__init__(self)
        self.name = "HashTag"
        # print "EdgeFeature HashTag initialized"

    def extract(self, nodeList, clique_size):
        assert len(nodeList) > 1
        for i in range(1, len(nodeList)):
            ancestors = []
            tmp = nodeList[i].parent
            for ans in range(1, clique_size):
                ancestors.append(tmp)
                tmp = nodeList[tmp].parent
                if tmp == -1:
                    break
            for j in ancestors:
                if len(set(nodeList[i].hashtag) & set(nodeList[j].hashtag)) > 0:
                    self.values[(j, i)] = 1
                else:
                    self.values[(j, i)] = 0
        for i in range(0, len(nodeList)):
            chdnList = nodeList[i].children
            if len(chdnList) <= 1:
                continue
            for ci in range(len(chdnList)):
                for cj in range(ci + 1, len(chdnList)):
                    if chdnList[ci] >= len(nodeList) or chdnList[cj] >= len(nodeList):
                        continue
                    if len(set(nodeList[chdnList[ci]].hashtag) & set(nodeList[chdnList[cj]].hashtag)) > 0:
                        self.values[(chdnList[ci], chdnList[cj])] = 1
                    else:
                        self.values[(chdnList[ci], chdnList[cj])] = 0


class SameEmoji(EdgeFeature):
    "test whether two nodes have the same emoji"

    def __init__(self):
        EdgeFeature.__init__(self)
        self.name = "SameEmoji"
        # print "EdgeFeature SameEmoji initialized"

    def extract(self, nodeList, clique_size):
        assert len(nodeList) > 1
        for i in range(1, len(nodeList)):
            ancestors = []
            tmp = nodeList[i].parent
            for ans in range(1, clique_size):
                ancestors.append(tmp)
                tmp = nodeList[tmp].parent
                if tmp == -1:
                    break
            for j in ancestors:
                if len(set(nodeList[i].emoji) & set(nodeList[j].emoji)) > 0:
                    self.values[(j, i)] = 1
                else:
                    self.values[(j, i)] = 0
        for i in range(0, len(nodeList)):
            chdnList = nodeList[i].children
            if len(chdnList) <= 1:
                continue
            for ci in range(len(chdnList)):
                for cj in range(ci + 1, len(chdnList)):
                    if chdnList[ci] >= len(nodeList) or chdnList[cj] >= len(nodeList):
                        continue
                    if len(set(nodeList[chdnList[ci]].emoji) & set(nodeList[chdnList[cj]].emoji)) > 0:
                        self.values[(chdnList[ci], chdnList[cj])] = 1
                    else:
                        self.values[(chdnList[ci], chdnList[cj])] = 0


class FollowRoot(EdgeFeature):
    "test whether this node has the same label as root"

    def __init__(self):
        EdgeFeature.__init__(self)
        self.name = "FollowRoot"
        # print "EdgeFeature FollowRoot initialized"

    def extract(self, nodeList, clique_size):
        assert len(nodeList) > 1
        root = nodeList[0]
        for i in range(1, len(nodeList)):
            ancestors = []
            tmp = nodeList[i].parent
            for ans in range(1, clique_size):
                ancestors.append(tmp)
                tmp = nodeList[tmp].parent
                if tmp == -1:
                    break
            for j in ancestors:
                if nodeList[j].number == 0:
                    self.values[(j, i)] = 1
                else:
                    self.values[(j, i)] = 0


class FollowFirst(EdgeFeature):
    def __init__(self):
        EdgeFeature.__init__(self)
        self.name = "FollowFirst"

    def extract(self, nodeList, clique_size):
        assert len(nodeList) > 1
        for i in range(1, len(nodeList)):
            tmp = nodeList[i].parent
            if tmp == 0:
                continue
            while nodeList[tmp].parent != 0:
                tmp = nodeList[tmp].parent
            self.values[(tmp, i)] = 1


def newFeature(featureName):
    return globals()[featureName]()