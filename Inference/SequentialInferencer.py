#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

from Inferencer import Inferencer


class SequentialInferencer(Inferencer):
    "predict labels of a thread sequentially from root to leaves"

    def __init__(self):
        self.name = "SequentialInferencer"

    def predict(self, thread):
        return None