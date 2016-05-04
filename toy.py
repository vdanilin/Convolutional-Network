# This is the basic idea behind the architecture

import numpy as np
import random
import math
import time
import scipy
from scipy import ndimage, misc
import matplotlib.pyplot as plt

im = scipy.ndimage.imread('cat.jpg', flatten=True)
print im.shape, type(im)
a = im.shape[0]
b= im.shape[1]
cat = scipy.misc.imresize(im, (a/40,b/40), interp='bilinear', mode=None)
print cat.shape

# normalize
cat = 1 - cat/255
print cat

# arr = np.zeros((cat2.shape[0], cat2.shape[1]))
# block_size = 4
# res = 0
# i= 0
# j = 0
# sub = 0
# k = 0
# while k < 10:
#     while i < cat2.shape[0] * cat2.shape[1]:
#         while j < 10:
#              sub += cat2[k][j]
#              j += 1
#              i += 1
#     arr.append(sub/block_size)
#     k += 2

# plt.imshow(cat2, cmap=plt.cm.gray, vmin=30, vmax=255)
# # plt.show()

# INPUT NEURONS = image
# cat = temp.reshape((temp.shape[0] * temp.shape[1], 1))


''' RECEPTIVE FIELD - WEIGHTS aka FILTER ->
initialize filters in a way that corresponds to the depth of the imagine.
If the input image is of channel 3 (RGB) then your weight vector is n*n*3.
PARAMETERS you'll need: DEPTH (num of filters), STRIDE (slide filter by), ZERO-PADDING(to control the spatial size of the output volumes). Use (Inputs-FilterSize + 2*Padding)/Stride + 1 to calculate your output volume and to decide your hyperparameters'''

DEPTH = 3
STRIDE = 2
# to ensure that the input and output volumes are the same: use P=(F-1)/2 given stride 1.
PADDING = 0
FILTER_SIZE = 5

class ToyNet(object):
    def __init__(self, sizes):
        self.sizes = sizes
        # initialize a list of filters
        self.weights = []
        for i in range(DEPTH):
            self.weights.append([np.random.randn(FILTER_SIZE, FILTER_SIZE)])
        self.biases = np.random.rand(DEPTH,1)
        self.activations = []

    def convolve(self, input_neurons):
        output_dim1 = (input_neurons.shape[0] - FILTER_SIZE + 2*PADDING)/STRIDE + 1
        output_dim2 =  (input_neurons.shape[1] - FILTER_SIZE + 2*PADDING)/STRIDE + 1

        for i in range(DEPTH):
            self.activations.append(np.empty((output_dim1 * output_dim2)))

        print 'shape of input: ', input_neurons.shape
        print 'shape of output: ', '(', output_dim1, output_dim2, ')'

        for i in range(DEPTH):
            slide = 0
            k = 0
            print self.activations[i].shape[0]
            while k < self.activations[i].shape[0]:  # check for last input element
                if FILTER_SIZE + slide < input_neurons.shape[0]:
                    self.activations[i][k] = np.sum(np.dot(input_neurons[slide:FILTER_SIZE + slide,slide:FILTER_SIZE + slide], self.weights[i][0])) + self.biases[i]
                else:
                    slide = 0
                    self.activations[i][k] = np.sum(np.dot(input_neurons[slide:FILTER_SIZE + slide,slide:FILTER_SIZE + slide], self.weights[i][0])) + self.biases[i]
                slide += STRIDE

                # print 'filter: ', i
                # print 'input matrix: ', input_neurons[slide:FILTER_SIZE + slide,slide:FILTER_SIZE + slide].shape
                # print 'weight matrix: ', self.weights[i][0].shape
                # print 'biases: ', self.biases[i].shape
                
                # if slide
                k += 1


            self.activations[i] = self.activations[i].reshape((output_dim1, output_dim2))
            print self.activations[i].shape
            print self.activations[0]

net = ToyNet([cat.shape[0]*cat.shape[1]])
print 'yooooo', net.sizes[0]
net.convolve(cat)