#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini

import sys
import math
import random
import traceback

def print_exc_plus():
    """
    Print the usual traceback information, followed by a listing of all the
    local variables in each frame.
    """
    tb = sys.exc_info()[2]
    while 1:
        if not tb.tb_next:
            break
        tb = tb.tb_next
    stack = []
    f = tb.tb_frame
    while f:
        stack.append(f)
        f = f.f_back
    stack.reverse()
    traceback.print_exc()
    print "Locals by frame, innermost last"
    for frame in stack:
        print
        print "Frame %s in %s at line %s" % (frame.f_code.co_name,
                                             frame.f_code.co_filename,
                                             frame.f_lineno)
        for key, value in frame.f_locals.items():
            print "\t%20s = " % key,
            #We have to be careful not to cause a new error in our error
            #printer! Calling str() on an unknown object could cause an
            #error we don't want.
            try:                   
                print value
            except:
                print "<ERROR WHILE PRINTING VALUE>"


def assertEqual(a, b, message=None):
    """
    Verbose assertEqual
    """
    if not message:
        message = "Was supposed %s == %s" % (a, b)
    if a != b:
        raise ValueError(message)

# calculate a random number where:  a <= rand < b
def rand(a, b):
    return (b-a)*random.random() + a

def dot(vec1, vec2):
    return sum([x * w for (x, w) in zip(vec1, vec2)])

def _vec(func):
    def __vec(vec1, vec2, out=None):
        if out == None:
            return [func(x, w) for (x, w) in zip(vec1, vec2)]
        else:
            for i in range(len(out)):
                out[i] = func(vec1[i], vec2[i])
            return out
    return __vec

def _map(func):
    def __map(vec, out=None):
        if out == None:
            return map(func, vec)
        else:
            for i in range(len(out)):
                out[i] = func(vec[i])
    return __map

def sigmoid(val):
    return 1.0 * (1.0 + math.exp(-val))
def sigmoid_deriv(val):
    return val * (1.0 - val)
sigmoid.deriv = sigmoid_deriv
sigmoid.vec = _vec(sigmoid)
sigmoid.map = _map(sigmoid)
sigmoid.deriv.vec = _vec(sigmoid_deriv)
sigmoid.deriv.map = _map(sigmoid_deriv)

def qloss(output, target):
    return sigmoid.deriv(output) * (output - target)
qloss.vec = _vec(qloss)

def diff(a, b):
    return a - b
diff.vec = _vec(diff)

def makeMatrix(rows, cols, fill=0.0):
    """
    >>> makeMatrix(2, 3)
    [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    >>> import random
    >>> random.seed(0)
    >>> makeMatrix(2, 3, random.random)
    [[0.84442185152504812, 0.75795440294030247, 0.420571580830845],\
 [0.25891675029296335, 0.51127472136860852, 0.40493413745041429]]
    """
    def _fill():
        return callable(fill) and fill() or fill
    matrix = []
    for i in range(rows):
        matrix.append([_fill() for j in range(cols)])
    return matrix


class Layer:
    def __init__(self, n_in, n_out):
        def _rand():
            return rand(-2.0, 2.0)
        self.n_in = n_in
        self.n_out = n_out
        self.inputs = [1.0]*n_in
        self.outputs = [1.0]*n_out # sigmoid(activations)
        self.weights = makeMatrix(n_out, n_in, _rand)
        self.delta_inputs = [0.0]*self.n_in
        self.delta_outputs = [0.0]*self.n_out
    def propagate(self, inputs=None):
        if inputs != None:
            if __debug__: assertEqual(len(inputs), self.n_in)
            self.inputs = inputs
        if __debug__: print "propagate(%s): outputs = %s ->" % (self.inputs, self.outputs),
        for k in range(self.n_out):
            self.outputs[k] = sigmoid(dot(self.weights[k], self.inputs))
        if __debug__: print "%s" % self.outputs
    def backPropagate(self, targets=None):
        if targets != None:
            if __debug__: assertEqual(len(targets), self.n_out)
            self.delta_outputs = diff.vec(self.outputs, targets)
        _weights = zip(*self.weights)
        if __debug__: print "backPropagate(%s): delta_inputs = %s ->" % (self.delta_outputs, self.delta_inputs),
        for j in range(1, self.n_in):
            self.delta_inputs[j] = sigmoid.deriv(self.inputs[j]) * dot(_weights[j], self.delta_outputs)
        if __debug__: print "%s" % self.delta_inputs
    def updateWeights(self, learn):
        # locals for performance or traceback
        # weights, deltas, inputs = self.weights, self.delta_inputs, self.inputs
        for j in range(self.n_in):
            for k in range(self.n_out):
                self.weights[k][j] -= learn * self.delta_outputs[k] * self.inputs[j]


class ShallowNetwork:
    def __init__(self, n_in, n_hid, n_out):
        n_in = n_in + 1 # bias
        self.in_layer = Layer(n_in, n_hid)
        self.out_layer = Layer(n_hid, n_out)
        self.in_layer.outputs = self.out_layer.inputs
        self.in_layer.delta_outputs = self.out_layer.delta_inputs
    def _propagate(self, inputs):
        self.in_layer.propagate(inputs + [1.0])
        self.out_layer.propagate()
    def _updateWeights(self, learn):
        self.in_layer.updateWeights(learn)
        self.out_layer.updateWeights(learn)
    def _backPropagate(self, targets, learn):
        self.out_layer.backPropagate(targets)
        self.in_layer.backPropagate()
        self._updateWeights(learn)
    def train(self, patterns, iterations=1000, learn=0.05):
        def sq2(x):
            return 0.5 * x**2
        for i in range(iterations):
            error = 0.0
            for inputs, targets in patterns:
                self._propagate(inputs)
                self._backPropagate(targets, learn)
                error += sum(map(sq2, self.out_layer.delta_outputs))
            if __debug__:
                print "iter(%s) error = %f" % (i, error)
    def test(self, patterns):
        for inputs, targets in patterns:
            self._propagate(inputs)
            res = self.out_layer.outputs
            print inputs, "->", res, "(%s)" % targets


def demo():
    # Teach network XOR function
    patterns = [
        [[0,0], [0]],
        [[0,1], [1]],
        [[1,0], [1]],
        [[1,1], [0]]
    ]

    # create a network with two input, two hidden, and two output nodes
    net = ShallowNetwork(2, 4, 1)
    # train it with some patterns
    net.train(patterns, 100)
    # test it
    net.test(patterns)
    
    
if __name__ == "__main__":
    if __debug__:
        import doctest
        doctest.testmod()
    try:
        demo()
    except:
        print_exc_plus()