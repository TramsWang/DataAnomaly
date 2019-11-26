import csv
import Divergence
import statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

reader = csv.reader(open("Correct/3.csv", 'r'))
data = list(int(row[2]) for row in reader)

reader_err = csv.reader(open("Centralized/3.csv", 'r'))
data_err = list(int(row[2]) for row in reader_err)

sigma = statistics.stdev(data)
step = 0.5 * sigma * (len(data) ** -0.2)

dropped, dist = Divergence.histogram(data, step)
dropped, dist_err = Divergence.histogram(data_err, step)

figure = plt.figure(figsize=(8, 4.5), dpi=100)
x = []
y = []
p = 0
for i in range(70):
    if i in dist:
        p += dist[i]
    x += [i, i+1]
    y += [p, p]
plt.plot(x, y, 'k', label="Correct")

x = []
y = []
p = 0
for i in range(70):
    if i in dist_err:
        p += dist_err[i]
    x += [i, i+1]
    y += [p, p]
plt.plot(x, y, 'r', label="Cheated")

plt.legend(fontsize='large')
plt.xlabel("Time Span", fontsize='x-large')
plt.ylabel("Cumulative Probability", fontsize='x-large')

figure.savefig("ExampleCDF.png")
