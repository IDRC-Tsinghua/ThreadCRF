#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'


class Weight:
    "describe the weights of features learned by crf model"

    def __init__(self, w_array, node_features, edge_features, dict_len):
        self.w_node = {}
        self.w_dict = {}
        pw = 0
        for feature in node_features:
            self.w_node[feature] = {}
        for i in range(1, dict_len + 1):
            self.w_dict[i] = {}
        for state in range(0, 3):
            for feature in node_features:
                self.w_node[feature][state] = w_array[pw]
                pw += 1
            for i in range(1, dict_len + 1):
                self.w_dict[i][state] = w_array[pw]
                pw += 1
        self.w_edge = {}
        for feature in edge_features:
            self.w_edge[feature] = {}
        for i in range(0, 3):
            for j in range(0, 3):
                for feature in edge_features:
                    self.w_edge[feature][(i, j)] = w_array[pw]
                    pw += 1
        assert pw == len(w_array)
