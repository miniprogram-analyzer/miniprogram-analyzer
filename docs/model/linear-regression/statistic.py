#!/usr/bin/python2
#coding:utf-8
from numpy import genfromtxt
import numpy
import matplotlib
matplotlib.use("Agg") # non-GUI env
from matplotlib import pyplot as plt

dataPath = r"../data/report.csv"
data = genfromtxt(dataPath, delimiter=",")

# .123
numpy.set_printoptions(precision=3)
# disable scientific notation
numpy.set_printoptions(suppress=True)

# print('cov')
# print(numpy.cov(data[:, 1:-1].T))

# print('corrcoef')
# corrcoef = numpy.corrcoef(data[:, 1:-1].T)
# print(corrcoef.shape)
# numpy.savetxt('corrcoef.csv', corrcoef, delimiter=',', fmt='%.3f')

print('max')
max = numpy.max(data[:, 1:-1], axis=0)
print(max)

print('min')
min = numpy.min(data[:, 1:-1], axis=0)
print(min)

print('mean')
mean = numpy.mean(data[:, 1:-1], axis=0)
print(mean)

print('median')
median = numpy.median(data[:, 1:-1], axis=0)
print(median)

print('var')
var = numpy.var(data[:, 1:-1], axis=0)
print(var)

############# box plot #####################
axe1 = plt.subplot(2, 3, 1)
axe1.set_title('pages')
plt.tight_layout()
plt.boxplot(data[:, 1])

axe2 = plt.subplot(2, 3, 2)
axe2.set_title('componentsCount')
plt.tight_layout()
plt.boxplot(data[:, 2])

axe3 = plt.subplot(2, 3, 3)
axe3.set_title('uniqueComponentsCount')
plt.tight_layout()
plt.boxplot(data[:, 3])


axe4 = plt.subplot(2, 3, 4)
axe4.set_title('wxAPIsCount')
plt.tight_layout()
plt.boxplot(data[:, 5])

axe5 = plt.subplot(2, 3, 5)
axe5.set_title('uniqueWxAPIsCount')
plt.tight_layout()
plt.boxplot(data[:, 6])

axe6 = plt.subplot(2, 3, 6)
axe6.set_title('CSSLOC')
plt.tight_layout()
plt.boxplot(data[:, 7])

plt.savefig('statistic')
