#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini

import os
import sys
if os.path.abspath("../") not in sys.path:
    sys.path.append(os.path.abspath("../"))
import bplnn
reload(bplnn)
from bplnn import *

def load_patterns(filename):
    trace("Loading '%s'" % filename)
    inputs = []
    targets = []
    for line in open(filename).readlines():
        row = map(int, line.split(","))
        stroke, number = row[:-1], row[-1]
        # normalize inputs
        inputs.append([float(i)/100 for i in stroke])
        # digitalize outputs
        targets.append([float(i == number) for i in range(10)])
    print stats(inputs, targets)
    print "-"*70
    #return np.mat(inputs) * 1.2 - 0.1, np.mat(targets) * 1.2 - 0.1
    return np.mat(inputs, dtype="float64"), np.mat(targets, dtype="float64")

def run():
    trace("PenDigits dataset", "#")
    inputs, targets = load_patterns("pendigits.tra")
    test_inputs, test_targets = load_patterns("pendigits.tes")
    n_in = inputs.shape[1] # 16
    n_out = targets.shape[1] # 10
    net = DeepNetwork([n_in, 20, 15, n_out])
    print net
    info(" auto train ".center(70, "-"))
    net.prepare(inputs, 200, 0.05, perturbate=0.1)
    info(" auto test ".center(70, "-"))
    net.test(test_inputs, test_targets)
    info(" classify train ".center(70, "-"))
    net.train(inputs, targets, 800, 0.1, saveimages=False)
    info(" classify test ".center(70, "-"))
    net.test(test_inputs, test_targets)


if __name__=="__main__":
    timed(run)

