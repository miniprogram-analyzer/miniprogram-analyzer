#!/usr/bin/python2
#coding:utf-8
from numpy import genfromtxt
import numpy
from sklearn import linear_model
from sklearn.externals import joblib
import matplotlib
matplotlib.use("Agg") # non-GUI env
from matplotlib import pyplot as plt
import time

dataPath = r"../data/report.csv"
deliveryData = genfromtxt(dataPath, delimiter=",")

print "data"
# print deliveryData

x= deliveryData[:, 1:-1]
y = deliveryData[:, -1]

print x
print y

lr = linear_model.LinearRegression()
lr.fit(x, y)

print lr
modelPath = r'./model/linear_model.pkl'
joblib.dump(lr, modelPath)

print("coefficients:")
print lr.coef_

print("intercept:")
print lr.intercept_

predictAll = map(lr.predict, map(lambda x : [x], x))

# print deliveryData[:, 0]
print predictAll

# # generate figures 
# plt.figure(1)
# plt.scatter(deliveryData[:, 0], y)
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("original score")
# plt.savefig("data")

# plt.figure(2)
# plt.scatter(deliveryData[:, 0], predictAll)
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("score prediction")
# plt.savefig("predict")

# plt.figure(3)
# plt.scatter(deliveryData[:, 0], deliveryData[:, 1])
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("pages")
# plt.savefig("pages")

# plt.figure(4)
# plt.scatter(deliveryData[:, 0], deliveryData[:, 2])
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("components")
# plt.savefig("componentsCount")

# plt.figure(5)
# plt.scatter(deliveryData[:, 0], deliveryData[:, 3])
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("unique components")
# plt.savefig("uniqueComponentsCount")

# plt.figure(6)
# plt.scatter(deliveryData[:, 0], deliveryData[:, 4])
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("enable cloudfunction")
# plt.savefig("hasCloudFunction")

# plt.figure(7)
# plt.scatter(deliveryData[:, 0], deliveryData[:, 5])
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("wx API Count")
# plt.savefig("wxAPIsCount")

# plt.figure(8)
# plt.scatter(deliveryData[:, 0], deliveryData[:, 6])
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("wx API category count")
# plt.savefig("uniqueWxAPIsCount")

# plt.figure(9)
# plt.scatter(deliveryData[:, 0], deliveryData[:, 7])
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("CSS Line of Code")
# plt.savefig("CSSLOC")

# plt.figure(10)
# plt.scatter(deliveryData[:, 0], y)
# plt.xlabel("ourspark miniprograms")
# plt.scatter(deliveryData[:, 0], predictAll)
# plt.ylabel("score: predict vs origin")
# plt.savefig("origin-predict-contrast")
