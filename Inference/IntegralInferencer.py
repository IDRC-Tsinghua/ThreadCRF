#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

from Inferencer import Inferencer


class IntegralInferencer(Inferencer):
    "predict labels of a thread as a whole"

    def __init__(self):
        self.name = "IntegralInferencer"

    def predict(self, thread):
        return None