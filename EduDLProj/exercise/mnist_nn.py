from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import random

from tensorflow.examples.tutorials.mnist import input_data

import matplotlib.pylab as plt
import tensorflow as tf


# Import data
flags = tf.app.flags
FLAGS = flags.FLAGS
# flags.DEFINE_string('data_dir', '/tmp/data/', 'Directory for storing data')
flags.DEFINE_string('data_dir', './MNIST_data/', 'Directory for storing data')

mnist = input_data.read_data_sets(FLAGS.data_dir, one_hot=True)

sess = tf.InteractiveSession()

# Create the model
X = tf.placeholder(tf.float32, [None, 784])
Y_ = tf.placeholder(tf.float32, [None, 10])

W1 = tf.get_variable("W1", shape=[784, 256], initializer=tf.contrib.layers.xavier_initializer(784, 256))
W2 = tf.get_variable("W2", shape=[256, 256], initializer=tf.contrib.layers.xavier_initializer(256, 256))
W3 = tf.get_variable("W3", shape=[256, 10], initializer=tf.contrib.layers.xavier_initializer(256, 10))

b1 = tf.Variable(tf.zeros([256]))
b2 = tf.Variable(tf.zeros([256]))
b3 = tf.Variable(tf.zeros([10]))

dropout_rate = tf.placeholder(tf.float32)

_L1 = tf.nn.relu(tf.matmul(X, W1) + b1)
L1 = tf.nn.dropout(_L1, dropout_rate)
L2 = tf.nn.relu(tf.matmul(L1, W2) + b2)
hypothesis = tf.nn.softmax(tf.matmul(L2, W3) + b3)

# Define loss and optimizer
cross_entropy = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=hypothesis, labels=Y_))
# train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)
train_step = tf.train.AdamOptimizer(0.01).minimize(cross_entropy)


# Train
tf.global_variables_initializer().run()

for i in range(5500):  # 5500
    batch_xs, batch_ys = mnist.train.next_batch(100)
    print("i : ", i, " batch_xs : ", batch_xs.shape, "batch_ys : ", batch_ys.shape)
    train_step.run({X: batch_xs, Y_: batch_ys, dropout_rate: 0.7})
    print ("cost : ", cross_entropy.eval({X: batch_xs, Y_: batch_ys, dropout_rate: 0.7}))
  
# Test trained model
correct_prediction = tf.equal(tf.argmax(hypothesis, 1), tf.argmax(Y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
print('accuracy : ', accuracy.eval({X: mnist.test.images, Y_: mnist.test.labels, dropout_rate: 0.7}))

r = random.randint(0, mnist.test.num_examples - 1)
print('Label : ', sess.run(tf.argmax(mnist.test.labels[r:r + 1], 1)))
print('Prediction : ', sess.run(tf.argmax(hypothesis, 1), {X:mnist.test.images[r:r + 1], dropout_rate: 0.7}))

plt.imshow(mnist.test.images[r:r + 1].reshape(28, 28)
           , cmap='Greys', interpolation='nearest')
plt.show()

