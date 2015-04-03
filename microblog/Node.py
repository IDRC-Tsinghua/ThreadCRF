#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'


class Node():
  nodeCount = 0

  def __init__(self, data):
    self.id = data['id']
    self.number = data['number']
    self.name = data['username']
    self.text = data['text']
    self.parent = data['parent']
    self.children = data['children']
    self.depth = data['depth']
    self.label = data['label']
    self.vector = None
    Node.nodeCount += 1

  def setVector(self, _vector):
    self.vector = _vector
