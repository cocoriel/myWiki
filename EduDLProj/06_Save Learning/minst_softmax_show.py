from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

# Import data
from tensorflow.examples.tutorials.mnist import input_data

import tensorflow as tf
import numpy as np
import random
import matplotlib.pylab as plt
from tensorflow.contrib.learn.python.learn.datasets import mnist

flags = tf.app.flags
FLAGS = flags.FLAGS
#flags.DEFINE_string('data_dir', '/tmp/data/', 'Directory for storing data')
flags.DEFINE_string('data_dir', './MNIST_data/', 'Directory for storing data')

mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

sess = tf.InteractiveSession()

# Create the model
x = tf.placeholder(tf.float32, [None, 784])
W = tf.Variable(tf.zeros([784, 10]))
b = tf.Variable(tf.zeros([10]))
y = tf.nn.softmax(tf.matmul(x, W) + b)

# Define loss and optimizer
y_ = tf.placeholder(tf.float32, [None, 10])
cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1])) #row
train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)

# Train
tf.global_variables_initializer().run()

for i in range(5500):  #5500
  batch_xs, batch_ys = mnist.train.next_batch(100)
  print("i",i, " batch_xs:",batch_xs.shape, "batch_ys", batch_ys.shape)
  train_step.run({x: batch_xs, y_: batch_ys})
  print ("cost:",cross_entropy.eval({x: batch_xs, y_: batch_ys}))
  
# Test trained model
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print(accuracy.eval({x: mnist.test.images, y_: mnist.test.labels}))

r = random.randint(0, mnist.test.num_examples -1)
print('Label:', sess.run(tf.argmax(mnist.test.labels[r:r+1],1)))
print('Prediction:', sess.run(tf.argmax(y,1),{x:mnist.test.images[r:r+1]}))

plt.imshow(mnist.test.images[r:r+1].reshape(28,28)
           , cmap='Greys', interpolation='nearest')
plt.show()

