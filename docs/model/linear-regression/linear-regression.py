from numpy import genfromtxt
import numpy
from sklearn import linear_model
import matplotlib
matplotlib.use('Agg') # non-GUI env
from matplotlib import pyplot as plt

import matplotlib.pyplot as plt

dataPath = r"./data/data.csv"
deliveryData = genfromtxt(dataPath, delimiter=',')

print "data"
print deliveryData

x= deliveryData[1:, :-1]
y = deliveryData[1:, -1]

print x
print y

lr = linear_model.LinearRegression()
lr.fit(x, y)

print lr

print("coefficients:")
print lr.coef_

print("intercept:")
print lr.intercept_

xPredict = [5, 1, 129]
xPredict = numpy.array(xPredict).reshape(1, -1)
yPredict = lr.predict(xPredict)
print("predict:")
print yPredict

print deliveryData[:, 0]
plt.scatter(deliveryData[:, 0], y)
# plt.show()
plt.savefig('data')
