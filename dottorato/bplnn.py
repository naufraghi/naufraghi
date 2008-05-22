#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Copyright (C) 2008 Matteo Bertini

import sys
import math
import time
import pprint

import numpy as np
from numpy import matlib
from numpy import random
import pylab

VERBOSE = 1

def debug(message):
    if VERBOSE > 1:
        print "DEBUG:", message
def info(message):
    if VERBOSE > 0:
        print "INFO:", message

def print_exc_plus():
    """
    Print the usual traceback information, followed by a listing of all the
    local variables in each frame.
    """
    import traceback
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


def stats(inputs, targets):
    return "\n".join(["patterns = %s" % len(inputs),
                      "features = %s" % len(inputs[0]),
                      "targets  = %s" % len(targets[0])])


def trace(s, sep='-'):
    s = (" %s " % s).center(70, sep)
    row = sep*len(s)
    info("\n".join([row, s, row]))


def assertEqual(a, b, message=None):
    """
    Verbose assertEqual
    """
    if not message:
        message = "Was supposed %s == %s" % (a, b)
    if a != b:
        raise ValueError(message)

def sigmoid(v):
    return 1.0 / (1.0 + np.exp(-v))
def sigmoid_deriv(v):
    return np.multiply(v, (1.0 - v))


class Layer:
    def __init__(self, n_in, n_out, linear=False):
        self.n_in = n_in
        self.n_out = n_out
        self.linear = linear
        self.inputs = None
        self.delta_inputs = None
        self.weights = np.mat(np.random.randn(n_in, n_out)*1.0)
        self.outputs = None
        self.delta_outputs = None
        self.targets = None
        self.errors = None
    def propagate(self, inputs):
        self.inputs = inputs
        #debug("inputs = %s\nweights = %s" % (self.inputs, self.weights))
        self.outputs = sigmoid(self.inputs*self.weights)
        #debug("outputs = %s" % self.outputs)
        return self.outputs
    def propagateBack(self, outputs):
        self.outputs = outputs
        #debug("outputs = %s\nweights.T = %s" % (self.outputs, self.weights.T))
        self.inputs = sigmoid(self.outputs*self.weights.T)
        #debug("inputs = %s" % self.inputs)
        return self.inputs
    def backPropagate(self, targets=None, delta_outputs=None):
        if targets != None:
            self.targets = targets
            #debug("targets = %s\noutputs = %s" % (self.targets, self.outputs))
            self.delta_outputs = np.multiply(sigmoid_deriv(self.outputs), (self.targets - self.outputs))
            #debug("delta_outputs = %s" % self.delta_outputs)
            self.errors = np.sum(np.mat(np.array(self.targets - self.outputs)**2), axis=1)
            #debug("errors = %s" % self.errors)
        elif delta_outputs != None:
            self.delta_outputs = delta_outputs
            #debug("delta_outputs = %s" % self.delta_outputs)
        else:
            raise ValueError("provide 'targets' or 'delta_outputs'")
        #debug("inputs = %s\ndelta_outputs = %s\nweights.T = %s" % (self.inputs, self.delta_outputs, self.weights.T))
        self.delta_inputs = np.multiply(sigmoid_deriv(self.inputs), (self.delta_outputs * self.weights.T))
        #debug("delta_inputs = %s\nerrors = %s" % (self.delta_inputs, self.errors))
        return self.delta_inputs
    def updateWeights(self, learn):
        #debug("inputs.T = %s\ndelta_outputs = %s" % (self.inputs.T, self.delta_outputs))
        self.weights += learn * (self.inputs.T * self.delta_outputs)
        #debug("weights = %s" % (self.weights))
        return self.weights
    def __repr__(self):
        return "<Layer %d %d>" % (self.n_in, self.n_out)
        
        
class AbstractNetwork:
    def train(self, inputs, targets, iterations=1000, learn=0.05):
        count = iterations
        step = 10 + int(math.sqrt(iterations))
        num = inputs.shape[0]
        batch_size = 1 + num / 20 # numbatches... tune it for you system/dataset
        info((" TRAIN batch_size=%s " % batch_size).center(70, "#"))
        ind = np.arange(num)
        for c, layer in enumerate(self.layers):
            pylab.imshow(layer.weights, cmap=pylab.cm.gray)
            pylab.savefig("(%1d) %s before" % (c, self))
        while count:
            count -= 1
            error = 0.0
            np.random.shuffle(ind)
            for batch in range(0, num, batch_size):
                selection = ind[batch:batch + batch_size]
                self.propagate(inputs[selection])
                self.backPropagate(targets[selection])
                error += self.errors.sum()
                self.updateWeights(learn)
            if not count % step:
                info("iter(%s) errors = %s" % (count, error))
        for c, layer in enumerate(self.layers):
            pylab.imshow(layer.weights, cmap=pylab.cm.gray)
            pylab.savefig("(%1d) %s post" % (c, self))
    def test(self, inputs, targets):
        info(" TEST ".center(70, "#"))
        def cls(arg):
            if arg.shape[1] == 1:
                return int(arg > 0.5)
            else:
                return arg.argmax()
        #for i in range(inputs.shape[0])[:10]:
        #    info("%s -> %s (%s)" % (inputs[i], cls(self.propagate(inputs[i])), cls(targets[i])))
        res = {}
        for i in range(inputs.shape[0]):
            output = cls(self.propagate(inputs[i]))
            target = cls(targets[i])
            res.setdefault(target, {True: 0.0, False: 0.0})
            res[target][target == output] += 1.0
            res[target]["acc"] = 100 * res[target][True] / (res[target][True] + res[target][False])
        info(pprint.pformat(res))
        info("mean acc = %f" % np.mean([res[t]["acc"] for t in res]))

class ShallowNetwork(AbstractNetwork):
    def __init__(self, n_in, n_hid, n_out, bias=True):
        self.bias = bias
        if bias:
            n_in = n_in + 1
        random.seed(123)
        self.layers = [Layer(n_in, n_hid), Layer(n_hid, n_out)]
    def propagate(self, inputs):
        if self.bias:
            inputs = np.append(inputs, np.ones((inputs.shape[0],1)), axis=1)
        #debug(" propagate IN ".center(70, "-"))
        hiddens = self.layers[0].propagate(inputs)
        #debug(" propagate OUT ".center(70, "-"))
        outputs = self.layers[1].propagate(hiddens)
        return outputs
    def propagateBack(self, outputs):
        #debug(" propagateBack IN ".center(70, "-"))
        hiddens = self.layers[1].propagateBack(outputs + 0.1 * np.random.rand(*outputs.shape))
        #debug(" propagateBack OUT ".center(70, "-"))
        inputs = self.layers[0].propagateBack(hiddens)
        if self.bias:
            inputs = inputs[:,:-1]
        return inputs
    def backPropagate(self, targets):
        #debug(" backPropagate OUT ".center(70, "-"))
        delta_inputs = self.layers[1].backPropagate(targets=targets)
        self.errors = self.layers[1].errors
        #debug(" backPropagate IN ".center(70, "-"))
        return self.layers[0].backPropagate(delta_outputs=delta_inputs)
    def updateWeights(self, learn):
        #debug(" updateWeights IN ".center(70, "-"))
        self.layers[0].updateWeights(learn)
        #debug(" updateWeights OUT ".center(70, "-"))
        self.layers[1].updateWeights(learn)
    def dump(self):
        return {"ShallowNetwork": self.layers}
    def __str__(self):
        return "<ShallowNetwork %s>" % self.layers


class DeepNetwork(AbstractNetwork):
    def __init__(self, n_nodes, bias=True):
        self.bias = bias
        if bias:
            n_nodes[0] += 1 # bias
        self.layers = [Layer(n_in, n_out) for n_in, n_out in zip(n_nodes[:-1], n_nodes[1:])]
        self.layers += [Layer(n_nodes[-1], n_nodes[-1])] # descramble autoencoder
    def propagate(self, inputs):
        if self.bias:
            inputs = np.append(inputs, np.ones((inputs.shape[0],1)), axis=1)
        outputs = self.layers[0].propagate(inputs)
        for layer in self.layers[1:]:
            outputs = layer.propagate(outputs)
        return outputs
    def backPropagate(self, targets):
        delta_inputs = self.layers[-1].backPropagate(targets=targets)
        self.errors = self.layers[-1].errors
        for layer in reversed(self.layers[:-1]):
            delta_inputs = layer.backPropagate(delta_outputs=delta_inputs)
        return delta_inputs
    def updateWeights(self, learn):
        for layer in self.layers:
            layer.updateWeights(learn)
    def prepare(self, inputs, targets, iterations, learn):
        info(" PREPARE ".center(70, "o"))
        if self.bias:
            inputs = np.append(inputs, np.ones((inputs.shape[0],1)), axis=1)
        iters = map(int, np.linspace(iterations, iterations/2, len(self.layers)))
        for c, layer in enumerate(self.layers[:-1]):
            info((" (%d) %s " % (c, layer)).center(70, "#"))
            auto_net = ShallowNetwork(layer.n_in, layer.n_out, layer.n_in, bias=False)
            auto_net.layers[1].weights = layer.weights.T
            auto_net.train(inputs, inputs, iters[c])
            layer.weights = auto_net.layers[1].weights.T
            auto_net.propagate(inputs)
            inputs = auto_net.layers[0].outputs
    def dump(self):
        return {"DeepNetwork": [l.dump() for l in self.layers]}
    def __str__(self):
        return "<DeepNetwork %s>" % str(self.layers)


def demo(iterations=1000, learn=0.05):
    # Teach network XOR function
    patterns = np.mat([[0.0,0.0, 0.0],
                       [0.0,1.0, 1.0],
                       [1.0,0.0, 1.0],
                       [1.0,1.0, 0.0]])

    _patterns = np.mat([[0.0,0.0, 0.0,0.0],
                       [0.0,1.0, 0.0,1.0],
                       [1.0,0.0, 1.0,0.0],
                       [1.0,1.0, 1.0,1.0]])
    inputs, targets = patterns[:,:-1], patterns[:,-1:]
    # create a network
    #net = ShallowNetwork(2, 5, 1)
    net = DeepNetwork([2, 5, 1])
    # train it with some patterns
    #for i in range(1):
    #    net.prepare(patterns, 50000, 0.05)
    # test it
    #print net.dump()
    #net.test(patterns)
    print net
    if isinstance(net, DeepNetwork):
        net.prepare(inputs, targets, iterations, learn)
    net.train(inputs, targets, iterations, learn)
    net.test(inputs, targets)
    return net


if __name__ == "__main__":
    if __debug__:
        import doctest
        doctest.testmod()
    try:
        start_time = time.time()
        demo()
        print "Time:", (time.time() - start_time)
    except:
        print_exc_plus()

