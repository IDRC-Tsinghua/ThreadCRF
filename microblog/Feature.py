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
  def __init__(self):
    NodeFeature.__init__(self)
    self.name = "NodeFeature: Root(yi)"
    print "NodeFeature Root(yi) initialized"


class SameAuthor(EdgeFeature):
  def __init__(self):
    EdgeFeature.__init__(self)
    self.name = "EdgeFeature: SameAuthor(yi,yj)"
    print "EdgeFeature SameAuthor(yi,yj) initialized"


def newFeature(featureName):
  return globals()[featureName]()