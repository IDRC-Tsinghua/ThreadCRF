#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'


class Feature:
  def __init__(self):
    self.name = "Feature"
    print "Feature initialized"

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
    self.values = {}
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
    self.values = {}
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


class SameAuthor(EdgeFeature):
  "test whether two nodes have the same author and the same label"

  def __init__(self):
    EdgeFeature.__init__(self)
    self.name = "EdgeFeature: SameAuthor(yi,yj)"
    self.values = {}
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
    self.values = {}
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