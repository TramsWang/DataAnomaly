import csv
import Divergence
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

day = 5

reader = csv.reader(open("Correct/%d.csv" % day, 'r'))
reader_cen = csv.reader(open("Centralized/%d.csv" % day, 'r'))
reader_equ = csv.reader(open("Equalized/%d.csv" % day, 'r'))

data = list(int(row[2]) for row in reader)
data_cen = list(int(row[2]) for row in reader_cen)
data_equ = list(int(row[2]) for row in reader_equ)

step = 1
print("Step: %f" % step)

hist = Divergence.histogram(data, step)
hist_cen = Divergence.histogram(data_cen, step)
hist_equ = Divergence.histogram(data_equ, step)

figure = plt.figure(figsize=(1800/300, 600/300), dpi=300)
plt.subplot(132)
x = []
y = []
for i in hist:
    x += [i]
    y += [hist[i]]
plt.bar(x, y, color='r', label="Correct")
plt.legend(fontsize="xx-small", loc="upper left")

plt.subplot(131)
x = []
y = []
for i in hist_cen:
    x += [i]
    y += [hist_cen[i]]
plt.bar(x, y, color='b', label="Centralized")
plt.legend(fontsize="xx-small", loc="upper left")

plt.subplot(133)
x = []
y = []
for i in hist_equ:
    x += [i]
    y += [hist[i]]
plt.bar(x, y, color='g', label="Equalized")
plt.legend(fontsize="xx-small", loc="upper left")

plt.savefig("SampleDay-%d.png" % day)
