#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'wangyc'

from Inferencer import Inferencer
from simanneal import Annealer
import random


class SimAnnealer(Annealer):
    def __init__(self, state, thread, inferencer):
        self.thread = thread
        self.inferencer = inferencer
        super(SimAnnealer, self).__init__(state)

    def move(self):
        i = random.randint(0, len(self.state) - 1)
        states = [0, 1, 2]
        states.remove(self.state[i])
        self.state[i] = random.choice(states)

    def energy(self):
        return -self.inferencer.computePotentials(self.thread, self.state) * 100


class IntegralInferencer(Inferencer, Annealer):
    "predict labels of a thread as a whole"

    def __init__(self, weight):
        Inferencer.__init__(self, weight)
        self.name = "IntegralInferencer"

    def predict(self, thread, init_state=None):
        self.thread = thread
        if init_state:
            assert len(init_state) == thread.nodeCount
        else:
            init_state = [1] * thread.nodeCount
        annealer = SimAnnealer(init_state, thread, self)
        annealer.Tmax = 5000
        best_state, potentials = annealer.anneal()
        print -potentials
        return best_state
