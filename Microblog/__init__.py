#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

WordMap = {}
index = 0
fin = open('../data/positive.txt', 'r')
line = fin.readline().strip()
while line:
    WordMap[int(line.split('\t')[0])] = index
    index += 1
    line = fin.readline().strip()
fin = open('../data/neutral.txt', 'r')
line = fin.readline().strip()
while line:
    WordMap[int(line.split('\t')[0])] = index
    index += 1
    line = fin.readline().strip()
fin = open('../data/negative.txt', 'r')
line = fin.readline().strip()
while line:
    WordMap[int(line.split('\t')[0])] = index
    index += 1
    line = fin.readline().strip()
