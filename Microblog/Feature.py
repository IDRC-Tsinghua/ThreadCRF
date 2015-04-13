#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

import math
from Emoji import *


class Feature:
    def __init__(self):
        self.name = "Feature"
        self.values = {}
        self.threshold = 0.2  # to be tuned
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

    def isAncestor(self, i, j, nodeList):
        "decide whether i is j's ancestor in the nodelist"
        curNode = nodeList[j]
        depth = 1
        while curNode.number != 0:
            if curNode.parent == i:
                return True, depth
            else:
                curNode = nodeList[curNode.parent]
                depth += 1
        if i == 0:
            return True, depth
        else:
            return False, -1

    def extract(self, nodeList):
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
        self.name = "NodeFeature: Root(yi)"
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
        self.name = "NodeFeature: Parent(yi)"
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
        self.name = "NodeFeature: ParentSim(yi)"
        # print "NodeFeature ParentSim(yi) initialized"

    def extract(self, nodeList):
        assert len(nodeList) > 0
        root = nodeList[0]
        self.values[root.number] = 0
        if len(nodeList) == 1:
            return
        for node in nodeList[1:]:
            if self.cosineSim(node.vector, nodeList[node.parent].vector) >= self.threshold \
                    and node.label == nodeList[node.parent].label:
                self.values[node.number] = 1
            else:
                self.values[node.number] = 0


class ParentDiff(NodeFeature):
    "test whether this node and its parent have very different text and different label"

    def __init__(self):
        NodeFeature.__init__(self)
        self.name = "NodeFeature: ParentDiff(yi)"
        # print "NodeFeature ParentDiff(yi) initialized"

    def extract(self, nodeList):
        assert len(nodeList) > 0
        root = nodeList[0]
        self.values[root.number] = 0
        if len(nodeList) == 1:
            return
        for node in nodeList[1:]:
            if self.cosineSim(node.vector, nodeList[node.parent].vector) <= self.threshold \
                    and node.label != nodeList[node.parent].label:
                self.values[node.number] = 1
            else:
                self.values[node.number] = 0


class SelfRepost(NodeFeature):
    "test whether this node and its parent are by the same author and have the same label"

    def __init__(self):
        NodeFeature.__init__(self)
        self.name = "NodeFeature: SelfRepost(yi)"
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
    "test whether this node's text and its possible emoji have the same label"

    def __init__(self):
        NodeFeature.__init__(self)
        self.name = "NodeFeature: NodeEmoji(yi)"
        # print "NodeFeature Emoji(yi) initialized"

    def extract(self, nodeList):
        assert len(nodeList) > 0
        for node in nodeList:
            # data['emoji'] is defined as a list of all emojis in the record
            if node.emoji:
                allEmoji = set(node.emoji)
                labelSum = 0
                for emoji in allEmoji:
                    labelSum += getEmojiLabel(emoji)
                if labelSum == 0:
                    emojiLabel = 0
                elif labelSum > 0:
                    emojiLabel = 1
                else:
                    emojiLabel = -1
                if node.label == emojiLabel:
                    self.values[node.number] = 1
                else:
                    self.values[node.number] = 0
            else:
                self.values[node.number] = 0


class SameAuthor(EdgeFeature):
    "test whether two nodes have the same author and the same label"

    def __init__(self):
        EdgeFeature.__init__(self)
        self.name = "EdgeFeature: SameAuthor(yi,yj)"
        # print "EdgeFeature SameAuthor(yi,yj) initialized"

    def extract(self, nodeList):
        assert len(nodeList) > 1
        for i in range(0, len(nodeList)):
            for j in range(i + 1, len(nodeList)):
                if nodeList[i].name == nodeList[j].name and nodeList[i].label == nodeList[j].label:
                    self.values[(nodeList[i].number, nodeList[j].number)] = 1
                else:
                    self.values[(nodeList[i].number, nodeList[j].number)] = 0


class Sibling(EdgeFeature):
    "test whether two nodes are siblings and have the same label"

    def __init__(self):
        EdgeFeature.__init__(self)
        self.name = "EdgeFeature: Sibling(yi,yj)"
        # print "EdgeFeature Sibling(yi,yj) initialized"

    def extract(self, nodeList):
        assert len(nodeList) > 1
        for i in range(0, len(nodeList)):
            for j in range(i + 1, len(nodeList)):
                if nodeList[i].parent == nodeList[j].parent and nodeList[i].label == nodeList[j].label:
                    self.values[(nodeList[i].number, nodeList[j].number)] = 1
                else:
                    self.values[(nodeList[i].number, nodeList[j].number)] = 0


class Similarity(EdgeFeature):
    "test whether two nodes have similar text and the same label"

    def __init__(self):
        EdgeFeature.__init__(self)
        self.name = "EdgeFeature: Similarity(yi,yj)"
        # print "EdgeFeature Similarity(yi,yj) initialized"

    def extract(self, nodeList):
        assert len(nodeList) > 1
        for i in range(0, len(nodeList)):
            for j in range(i + 1, len(nodeList)):
                if self.cosineSim(nodeList[i].vector, nodeList[j].vector) >= self.threshold \
                        and nodeList[i].label == nodeList[j].label:
                    self.values[(nodeList[i].number, nodeList[j].number)] = math.exp(1 - self.distance(i, j, nodeList))
                else:
                    self.values[(nodeList[i].number, nodeList[j].number)] = 0


class SentimentProp(EdgeFeature):
    "test the sentiment propagation relation in routes"

    def __init__(self):
        EdgeFeature.__init__(self)
        self.name = "EdgeFeature: SentimentProp(yi,yj)"
        # print "EdgeFeature SentimentProp(yi,yj) initialized"

    def extract(self, nodeList):
        assert len(nodeList) > 1
        for i in range(0, len(nodeList)):
            for j in range(i + 1, len(nodeList)):
                isAnc, distance = self.isAncestor(i, j, nodeList)
                if isAnc:
                    self.values[(nodeList[i].number, nodeList[j].number)] = math.exp(1 - distance)
                else:
                    self.values[(nodeList[i].number, nodeList[j].number)] = 0


class AuthorRef(EdgeFeature):
    "test whether the node's author is mentioned by its ancestor and they have the same label"

    def __init__(self):
        EdgeFeature.__init__(self)
        self.name = "EdgeFeature: AuthorRef(yi,yj)"
        # print "EdgeFeature AuthorRef(yi,yj) initialized"

    def extract(self, nodeList):
        assert len(nodeList) > 1
        for i in range(0, len(nodeList)):
            for j in range(i + 1, len(nodeList)):
                if nodeList[i].label == nodeList[j].label and nodeList[j].name in nodeList[i].mention:
                    isAnc, distance = self.isAncestor(i, j, nodeList)
                    if isAnc:
                        self.values[(nodeList[i].number, nodeList[j].number)] = 1
                    else:
                        self.values[(nodeList[i].number, nodeList[j].number)] = 0
                else:
                    self.values[(nodeList[i].number, nodeList[j].number)] = 0


class HashTag(EdgeFeature):
    "test whether two nodes have the same hashtag and label"

    def __init__(self):
        EdgeFeature.__init__(self)
        self.name = "EdgeFeature: HashTag(yi,yj)"
        # print "EdgeFeature AuthorRef(yi,yj) initialized"

    def extract(self, nodeList):
        assert len(nodeList) > 1
        for i in range(0, len(nodeList)):
            for j in range(i + 1, len(nodeList)):
                if nodeList[i].label == nodeList[j].label and \
                                len(set(nodeList[i].hashtag) & set(nodeList[j].hashtag)) > 0:
                    self.values[(nodeList[i].number, nodeList[j].number)] = 1
                else:
                    self.values[(nodeList[i].number, nodeList[j].number)] = 0


class SameEmoji(EdgeFeature):
    "test whether two nodes have the same emoji and label"

    def __init__(self):
        EdgeFeature.__init__(self)
        self.name = "EdgeFeature: SameEmoji(yi,yj)"
        # print "EdgeFeature AuthorRef(yi,yj) initialized"

    def extract(self, nodeList):
        assert len(nodeList) > 1
        for i in range(0, len(nodeList)):
            for j in range(i + 1, len(nodeList)):
                if nodeList[i].label == nodeList[j].label and \
                                len(set(nodeList[i].emoji) & set(nodeList[j].emoji)) > 0:
                    self.values[(nodeList[i].number, nodeList[j].number)] = 1
                else:
                    self.values[(nodeList[i].number, nodeList[j].number)] = 0


def newFeature(featureName):
    return globals()[featureName]()