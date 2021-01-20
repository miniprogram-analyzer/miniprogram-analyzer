#!/usr/bin/python
#coding:utf-8
from numpy import genfromtxt
import numpy
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.externals import joblib
import matplotlib
matplotlib.use("Agg") # non-GUI env
from matplotlib import pyplot as plt

# data
dataPath = r"../data/report_with_human_score.csv"
data = genfromtxt(dataPath, delimiter=",")

# data -> x + y
# x = data[:, 1:-1]
x = []
for i in range(len(data)):
  x.append(data[i][1:4] + data[i][5:8])
y = data[:, -1]

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

# standardization
sc = StandardScaler()
sc.fit(x_train)
x_train_std = sc.transform(x_train)
x_test_std = sc.transform(x_test)

# linear regression model
lr = linear_model.LinearRegression()
lr.fit(x_train_std, y_train)

# save model
modelPath = r'./model/linear_model.pkl'
joblib.dump(lr, modelPath)

# results
print("coefficients: ", lr.coef_, "intercept: ", lr.intercept_)
print("score: ", lr.score(x_test_std, y_test))

predictAll = map(lr.predict, map(lambda x_test_std : [x_test_std], x_test_std))

# # generate figures 
# plt.figure(1)
# plt.scatter(data[:, 0], y)
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("original score")
# plt.savefig("data")

# plt.figure(2)
# plt.scatter(data[:, 0], predictAll)
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("score prediction")
# plt.savefig("predict")

# plt.figure(3)
# plt.scatter(data[:, 0], data[:, 1])
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("pages")
# plt.savefig("pages")

# plt.figure(4)
# plt.scatter(data[:, 0], data[:, 2])
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("components")
# plt.savefig("componentsCount")

# plt.figure(5)
# plt.scatter(data[:, 0], data[:, 3])
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("unique components")
# plt.savefig("uniqueComponentsCount")

# plt.figure(6)
# plt.scatter(data[:, 0], data[:, 4])
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("enable cloudfunction")
# plt.savefig("hasCloudFunction")

# plt.figure(7)
# plt.scatter(data[:, 0], data[:, 5])
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("wx API Count")
# plt.savefig("wxAPIsCount")

# plt.figure(8)
# plt.scatter(data[:, 0], data[:, 6])
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("wx API category count")
# plt.savefig("uniqueWxAPIsCount")

# plt.figure(9)
# plt.scatter(data[:, 0], data[:, 7])
# plt.xlabel("ourspark miniprograms")
# plt.ylabel("CSS Line of Code")
# plt.savefig("CSSLOC")

plt.figure(10)
plt.scatter(range(len(y_test)), y_test)
plt.xlabel("ourspark miniprograms")
plt.scatter(range(len(y_test)), predictAll)
plt.ylabel("score: predict vs origin")
plt.savefig("origin-predict-contrast")
