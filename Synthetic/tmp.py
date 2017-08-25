import csv
import Divergence
import statistics
import random
import scipy.stats as stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math
import sys


reader = csv.reader(open("Correct/92.csv", 'r'))
data = list(int(row[2]) for row in reader)
reader = csv.reader(open("Centralized/92.csv", 'r'))
data_cen = list(int(row[2]) for row in reader)
step = 1403

dropped, dist = Divergence.histogram(data, step)
dropped, dist_cen = Divergence.histogram(data_cen, step)

figure = plt.figure(figsize=(1500/300, 900/300), dpi=300)
acc = 0
x = []
ecdf = []
for i in range(60):
    if i in dist:
        acc += dist[i]
    x += [i, i+1]
    ecdf += [acc, acc]
plt.plot(x, ecdf, 'k', label="Correct")

acc = 0
x = []
ecdf = []
for i in range(60):
    if i in dist_cen:
        acc += dist_cen[i]
    x += [i, i+1]
    ecdf += [acc, acc]
plt.plot(x, ecdf, 'r', label="Cheated")
plt.legend()
plt.grid()
figure.savefig("ECDF.png")