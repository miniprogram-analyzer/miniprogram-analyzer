#!/usr/bin/python
#coding:utf-8
from numpy import genfromtxt
import numpy
from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
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

y = map(lambda i:(i-80)/5, y)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=0)

# standardization
sc = StandardScaler()
sc.fit(x_train)
x_train_std = sc.transform(x_train)
x_test_std = sc.transform(x_test)

# linear regression model
lr = linear_model.LogisticRegression()
lr.fit(x_train_std, y_train)

# results
print("coefficients: ", lr.coef_, "intercept: ", lr.intercept_)
accuracy = lr.score(x_test_std, y_test)
print("accuracy: ", accuracy)

# figures
predictAll = map(lr.predict, map(lambda x_test_std : [x_test_std], x_test_std))
plt.scatter(range(len(y_test)), y_test)
plt.xlabel("ourspark miniprograms")
plt.scatter(range(len(y_test)), predictAll)
plt.ylabel("score: predict vs origin")
plt.savefig("origin-predict-contrast")
