#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

from Emoji import *
import pdb

class Node:
    nodeCount = 0

    def __init__(self, data):
        self.id = int(data['threadid'])
        self.number = int(data['docid'])
        self.name = data['username']
        self.parent = int(data['parent'])
        self.depth = int(data['depth'])
        self.label = int(data['label']) + 1

        if 'children' in data:
            self.children = []
            tmp = data['children'].encode('utf-8')
            if len(tmp) > 0:
                for num in tmp.split(','):
                    self.children.append(int(num))

        if 'vector' in data:
            self.vector = {}
            for pair in data['vector']:
                self.vector[pair[0]] = pair[1]
        else:
            self.vector = {}

        if 'emoji' in data:
            self.emoji = data['emoji']
        else:
            self.emoji = []

        if 'mention' in data:
            self.mention = data['mention']
        else:
            self.mention = []

        if 'hashtag' in data:
            self.hashtag = data['hashtag']
        else:
            self.hashtag = []

        Node.nodeCount += 1

    def setVector(self, _vector):
        self.vector = _vector

    def setEmoji(self, _emoji):
        self.emoji = _emoji

    def setMention(self, _mention):
        self.mention = _mention

    def setHashTag(self, _hashtag):
        self.hashtag = _hashtag

    def toVector(self, length):
        vec = [0 for i in range(length)]
        """for index in self.vector.keys():
            if not index in WordMap.keys():
                continue
            vec[WordMap[index]] = self.vector[index]"""
        for index in self.vector:
            assert index < length
            vec[index] = self.vector[index]
        pos = len(positiveEmoji)
        neu = len(neutralEmoji)
        neg = len(negativeEmoji)
        for e in self.emoji:
            e = e.encode('utf-8')
            if e in positiveEmoji:
                vec[length - neg - neu - pos + positiveEmoji.index(e)] += 1
            elif e in neutralEmoji:
                vec[length - neg - neu + neutralEmoji.index(e)] += 1
            elif e in negativeEmoji:
                vec[length - neg + negativeEmoji.index(e)] += 1
        return vec
