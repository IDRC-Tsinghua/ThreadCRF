#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

import math
from Emoji import *

class Feature:
  def __init__(self):
    self.name = "Feature"
    self.values = {}
    self.threshold = 0.5  # to be tuned
    print "Feature initialized"

  def cosineSim(self, A, B):
    assert len(A) == len(B)
    sum_AB = 0.0
    sum_A2 = 0.0
    sum_B2 = 0.0
    for i in range(len(A)):
      sum_AB += A[i] * B[i]
      sum_A2 += A[i] ** 2
      sum_B2 += B[i] ** 2
    return sum_AB / (math.sqrt(sum_A2) * math.sqrt(sum_B2))

  def extract(self, nodeList):
    return

  def __del__(self):
    print "Feature destroyed"


class NodeFeature(Feature):
  def __init__(self):
    Feature.__init__(self)
    self.name = "NodeFeature"
    print "NodeFeature initialized"

  def __del__(self):
    print "NodeFeature destroyed"


class EdgeFeature(Feature):
  def __init__(self):
    Feature.__init__(self)
    self.name = "EdgeFeature"
    print "EdgeFeature initialized"

  def __del__(self):
    print "EdgeFeature destroyed"


class Root(NodeFeature):
  "test whether this node has the same label as root"

  def __init__(self):
    NodeFeature.__init__(self)
    self.name = "NodeFeature: Root(yi)"
    print "NodeFeature Root(yi) initialized"

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
    print "NodeFeature Parent(yi) initialized"

  def extract(self, nodeList):
    assert len(nodeList) > 0
    root = nodeList[0]
    self.values[root.number] = 1
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
    print "NodeFeature ParentSim(yi) initialized"

  def extract(self, nodeList):
    assert len(nodeList) > 0
    root = nodeList[0]
    self.values[root.number] = 1
    if len(nodeList) == 1:
      return
    for node in nodeList[1:]:
      if self.cosineSim(node.vector, nodeList[node.parent].vector) >= self.threshold \
          and node.label == nodeList[node.parent].label:
        self.values[node.number] = 1
      else:
        self.values[node.number] = 0


class Emoji(NodeFeature):
  "test whether this node's text and its possible emoji have the same label"

  def __init__(self):
    NodeFeature.__init__(self)
    self.name = "NodeFeature: Emoji(yi)"
    print "NodeFeature Emoji(yi) initialized"

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
    print "EdgeFeature SameAuthor(yi,yj) initialized"

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
    print "EdgeFeature Sibling(yi,yj) initialized"

  def extract(self, nodeList):
    assert len(nodeList) > 1
    for i in range(0, len(nodeList)):
      for j in range(i + 1, len(nodeList)):
        if nodeList[i].parent == nodeList[j].parent and nodeList[i].label == nodeList[j].label:
          self.values[(nodeList[i].number, nodeList[j].number)] = 1
        else:
          self.values[(nodeList[i].number, nodeList[j].number)] = 0


def newFeature(featureName):
  return globals()[featureName]()