import tensorflow as tf   # 使用tensorflow1.9版本
import csv
import numpy as np
from keras.utils import to_categorical # version: 2.2 与 tensorflow 1.9 兼容
import matplotlib
matplotlib.use("Agg") # non-GUI env
import matplotlib.pyplot as plt


# 数据文件路径
path = "../data/report_with_label.csv"


seed = 5
seed1 = 67

# 输入7个属性值
input_node = 7
# 设置了两层神经网络，分别是12、32个神经元
layer = 12
layer1 = 32
# 输出的是成绩级别：合格，良，好，优秀
output_node = 4
# 学习率
learning_rate = 0.001
batch_size = 8
# 训练次数
steps = 3000
# 训练集个数
train_data_size = 80
# 正则化参数
REGULARIZATION_RAZE = 0.03
keep = 0.998

# 读取csv文件的7个属性值
ID = []
data = []
target = []
reader = csv.reader(open(path))
for line in reader:
    line = list(map(float, line))
    ID.append(line[0])
    data.append(line[1:8])
    target.append(int(line[-1]))

# 设置随机数
np.random.seed(seed)
np.random.shuffle(data)
np.random.seed(seed)
np.random.shuffle(target)
np.random.seed(seed)

# 分配训练集和测试集
x_train = data[:train_data_size]
y_train = np.array(target[:train_data_size])
x_test = data[train_data_size:]
y_test = np.array(target[train_data_size:])
# 将标签转换为one-hot码
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# 建立神经网络参数
w11 = tf.Variable(tf.random_normal([input_node, layer], stddev=0.1, seed=seed1))
b11 = tf.Variable(tf.random_normal([1, layer], stddev=0.1, seed=seed1))
w21 = tf.Variable(tf.random_normal([layer, layer1], stddev=0.1, seed=seed1))
b21 = tf.Variable(tf.random_normal([1, layer1], stddev=0.1, seed=seed1))
w31 = tf.Variable(tf.random_normal([layer1, output_node], stddev=0.1, seed=seed1))
b31 = tf.Variable(tf.random_normal([1, output_node], stddev=0.1, seed=seed1))

# 初始化输入输出占位符
x = tf.placeholder(tf.float32, shape=(None, input_node), name="x_input")
y_ = tf.placeholder(tf.float32, shape=(None, output_node), name="y_input")
keep_prob = tf.placeholder(tf.float32)

# 每层神经网络的输出计算公式
y1 = tf.nn.relu(tf.nn.dropout(tf.add(tf.matmul(x, w11), b11), keep_prob))
y1 = tf.nn.relu(tf.nn.dropout(tf.add(tf.matmul(y1, w21), b21), keep_prob))
y1 = tf.nn.dropout(tf.add(tf.matmul(y1, w31), b31), keep_prob)
y = tf.nn.softmax(y1)

# 定义损失函数
cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=y1, labels=y_)
cross_entropy_mean = tf.reduce_mean(cross_entropy)
regularization = tf.contrib.layers.l2_regularizer(REGULARIZATION_RAZE)(w11) + tf.contrib.layers.l2_regularizer(REGULARIZATION_RAZE)(w21) + tf.contrib.layers.l2_regularizer(REGULARIZATION_RAZE)(w31)
loss = cross_entropy_mean + regularization

# 使用AdamOptimizer优化器训练
train_step = tf.train.AdamOptimizer(learning_rate).minimize(loss)

# 计算准确率
correct_prediction = tf.equal(tf.argmax(y, 1), tf.argmax(y_, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

# 开始训练
with tf.Session() as sess:
    tf.global_variables_initializer().run()
    lo = []
    # 训练steps轮
    for i in range(steps):
        for j in range(10):
            start = j * batch_size
            end = start + 8
            validate_feed_batch = {x: x_train[start:end], y_: y_train[start:end], keep_prob: keep}
            sess.run(train_step, feed_dict=validate_feed_batch)
        # 计算loss
        l = sess.run(loss, feed_dict=validate_feed_batch)
        lo.append(l)
        validate_feed = {x: x_train, y_: y_train, keep_prob: keep}
        validate_acc = sess.run(accuracy, feed_dict=validate_feed_batch)
        test_feed = {x: x_test, y_: y_test, keep_prob: 1}
        # 计算准确率
        test_acc = sess.run(accuracy, feed_dict=test_feed)
        print("After %d training step(s), validation_accuracy is %g, test_accuracy is %g " % (i, validate_acc, test_acc))
    sample = np.arange(steps)
    # 可视化输出
    plt.plot(sample, lo, marker="*", linewidth=1, linestyle="--", color="red")
    plt.title("DNN")
    plt.xlabel("Sampling Point")
    plt.ylabel("Loss")
    plt.grid(True)
    plt.show()
    plt.savefig('loss_of_samples')

