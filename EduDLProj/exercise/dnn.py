import tensorflow as tf
import numpy as np

xy = np.loadtxt("../data/07train.txt")
x_data = xy[:, :-1]
y_data = xy[:, [-1]]

X = tf.placeholder(tf.float32, [None, 2])
Y = tf.placeholder(tf.float32, [None, 1])

W1 = tf.Variable(tf.random_normal([2, 5]))
W2 = tf.Variable(tf.random_normal([5, 4]))
W3 = tf.Variable(tf.random_normal([4, 1]))

b1 = tf.Variable(tf.random_normal([5]))
b2 = tf.Variable(tf.random_normal([4]))
b3 = tf.Variable(tf.random_normal([1]))


L1 = tf.sigmoid(tf.matmul(X, W1) + b1)
L2 = tf.sigmoid(tf.matmul(L1, W2) + b2)
hypothesis = tf.sigmoid(tf.matmul(L2, W3) + b3)

cost = -tf.reduce_mean(Y * tf.log(hypothesis) + (1 - Y) * tf.log(1 - hypothesis))

train = tf.train.GradientDescentOptimizer(0.1).minimize(cost)

sess = tf.Session()
sess.run(tf.global_variables_initializer())

for step in range(5001):
    sess.run(train, feed_dict={X:x_data, Y:y_data})
    if step % 100 == 0:
        print('step : ', step, 'cost : ', sess.run(cost, feed_dict={X:x_data, Y:y_data}), 
              '\nWeight : \n', sess.run(W1), sess.run(W2), sess.run(W3), 
              '\nbias : \n', sess.run(b1), sess.run(b2), sess.run(b3))

predicted = tf.cast(hypothesis > 0.5, tf.float32)
accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, Y), tf.float32))
        
h, p, a = sess.run([hypothesis, predicted, accuracy], feed_dict={X:x_data, Y:y_data})        
print('\nhypothesis\n', h, '\npredicted\n', p, '\nrealvalue\n', y_data, '\naccuracy\n', a)