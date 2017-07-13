import tensorflow as tf
import numpy as np

xy = np.loadtxt("../data/07train.txt")
x_data = xy[:, :-1]
y_data = xy[:, [-1]]

X = tf.placeholder(tf.float32, [None, 2])
Y = tf.placeholder(tf.float32, [None, 1])

W1 = tf.Variable(tf.random_normal([2, 10]))
W2 = tf.Variable(tf.random_normal([10, 10]))
W3 = tf.Variable(tf.random_normal([10, 10]))
W4 = tf.Variable(tf.random_normal([10, 10]))
W5 = tf.Variable(tf.random_normal([10, 10]))
W6 = tf.Variable(tf.random_normal([10, 10]))
W7 = tf.Variable(tf.random_normal([10, 10]))
W8 = tf.Variable(tf.random_normal([10, 10]))
W9 = tf.Variable(tf.random_normal([10, 1]))



b1 = tf.Variable(tf.random_normal([10]))
b2 = tf.Variable(tf.random_normal([10]))
b3 = tf.Variable(tf.random_normal([10]))
b4 = tf.Variable(tf.random_normal([10]))
b5 = tf.Variable(tf.random_normal([10]))
b6 = tf.Variable(tf.random_normal([10]))
b7 = tf.Variable(tf.random_normal([10]))
b8 = tf.Variable(tf.random_normal([10]))
b9 = tf.Variable(tf.random_normal([1]))


L1 = tf.sigmoid(tf.matmul(X, W1) + b1)
L2 = tf.sigmoid(tf.matmul(L1, W2) + b2)
L3 = tf.sigmoid(tf.matmul(L2, W3) + b3)
L4 = tf.sigmoid(tf.matmul(L3, W4) + b4)
L5 = tf.sigmoid(tf.matmul(L4, W5) + b5)
L6 = tf.sigmoid(tf.matmul(L5, W6) + b6)
L7 = tf.sigmoid(tf.matmul(L6, W7) + b7)
L8 = tf.sigmoid(tf.matmul(L7, W8) + b8)
hypothesis = tf.sigmoid(tf.matmul(L8, W9) + b9)

cost = -tf.reduce_mean(Y * tf.log(hypothesis) + (1 - Y) * tf.log(1 - hypothesis))

train = tf.train.GradientDescentOptimizer(0.4).minimize(cost)

sess = tf.Session()
sess.run(tf.global_variables_initializer())

for step in range(5001):
    sess.run(train, feed_dict={X:x_data, Y:y_data})
    if step % 100 == 0:
        print('step : ', step, 'cost : ', sess.run(cost, feed_dict={X:x_data, Y:y_data})) 
#               '\nWeight : \n', sess.run(W1), sess.run(W3), sess.run(W9), 
#               '\nbias : \n', sess.run(b1), sess.run(b3), sess.run(b9))

predicted = tf.cast(hypothesis > 0.5, tf.float32)
accuracy = tf.reduce_mean(tf.cast(tf.equal(predicted, Y), tf.float32))
        
h, p, a = sess.run([hypothesis, predicted, accuracy], feed_dict={X:x_data, Y:y_data})        
print('\nhypothesis\n', h, '\npredicted\n', p, '\nrealvalue\n', y_data, '\naccuracy\n', a)