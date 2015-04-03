#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

from Node import *
from Feature import *


class Thread:
  threadCount = 0

  def __init__(self, _id, nodeList):
    assert len(nodeList) > 0
    self.id = _id
    self.nodes = nodeList
    self.nodeCount = len(self.nodes)
    self.nodeFeatures = {}
    self.edgeFeatures = {}
    Thread.threadCount += 1

  def setNodeFeatures(self, featureNames=[]):
    for feature in featureNames:
      nodeFeature = newFeature(feature)
      self.nodeFeatures[feature] = nodeFeature

  def setEdgeFeatures(self, featureNames=[]):
    for feature in featureNames:
      edgeFeature = newFeature(feature)
      self.edgeFeatures[feature] = edgeFeature

  def extractNodeFeatures(self):
    for nodeFeature in self.nodeFeatures:
      nodeFeature.extract(self.nodes)

  def extractEdgeFeatures(self):
    for edgeFeature in self.edgeFeatures:
      edgeFeature.extract(self.nodes)

  def extractFeatures(self, nodeFeatureNames=[], edgeFeatureNames=[]):
    if len(nodeFeatureNames) > 0:
      self.setNodeFeatures(nodeFeatureNames)
    if len(edgeFeatureNames) > 0:
      self.setEdgeFeatures(edgeFeatureNames)
    self.extractNodeFeatures()
    self.extractEdgeFeatures()


if __name__ == '__main__':
  data = {'id': 123456, 'number': 0, 'text': '哈哈', 'parent': -1, 'children': [1, 2], 'depth': 0}
  root = Node(data)
  thread = Thread(123456, [root])
  thread.setNodeFeatures(['Root'])
  thread.setEdgeFeatures(['SameAuthor'])
