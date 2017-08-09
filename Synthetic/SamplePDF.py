import csv
import Divergence
import statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

day = 92

reader = csv.reader(open("Correct/%d.csv" % day, 'r'))
reader_cen = csv.reader(open("Centralized/%d.csv" % day, 'r'))
reader_equ = csv.reader(open("Equalized/%d.csv" % day, 'r'))

# Calculate distribution
data = list(int(row[2]) for row in reader)
data_cen = list(int(row[2]) for row in reader_cen)
data_equ = list(int(row[2]) for row in reader_equ)

sigma = statistics.stdev(data)
step = 0.5 * sigma * (len(data) ** -0.2)
print("Step: %f" % step)

hist, dist = Divergence.histogram(data, step)
hist_cen, dist_cen = Divergence.histogram(data_cen, step)
hist_equ, dist_equ = Divergence.histogram(data_equ, step)

# Calculate 2nd order distribution
data2 = list(hist.values())
data_cen2 = list(hist_cen.values())
data_equ2 = list(hist_equ.values())

sigma2 = statistics.stdev(data2)
step2 = 0.5 * sigma2 * (len(data2) ** -0.2)
print("Step2: %f" % step2)

hist2, dist2 = Divergence.histogram(data2, step2)
hist_cen2, dist_cen2 = Divergence.histogram(data_cen2, step2)
hist_equ2, dist_equ2 = Divergence.histogram(data_equ2, step2)

# Plot
figure = plt.figure(figsize=(1800/300, 1200/300), dpi=300)
# Plot distributions
plt.subplot(231)
x = []
y = []
for i in hist_cen:
    x += [i]
    y += [hist_cen[i]]
plt.bar(x, y, color='b', label="Centralized")
plt.legend(fontsize="xx-small", loc="upper left")

plt.subplot(232)
x = []
y = []
for i in hist:
    x += [i]
    y += [hist[i]]
plt.bar(x, y, color='r', label="Correct")
plt.legend(fontsize="xx-small", loc="upper left")
plt.title("1st Order")

plt.subplot(233)
x = []
y = []
for i in hist_equ:
    x += [i]
    y += [hist_equ[i]]
plt.bar(x, y, color='g', label="Equalized")
plt.legend(fontsize="xx-small", loc="upper left")

# Plot 2nd order distributions
plt.subplot(234)
x = []
y = []
for i in hist_cen2:
    x += [i]
    y += [hist_cen2[i]]
plt.bar(x, y, color='b', label="Centralized")
plt.legend(fontsize="xx-small", loc="upper left")

plt.subplot(235)
x = []
y = []
for i in hist2:
    x += [i]
    y += [hist2[i]]
plt.bar(x, y, color='r', label="Correct")
plt.legend(fontsize="xx-small", loc="upper left")
plt.title("1st Order")

plt.subplot(236)
x = []
y = []
for i in hist_equ2:
    x += [i]
    y += [hist_equ2[i]]
plt.bar(x, y, color='g', label="Equalized")
plt.legend(fontsize="xx-small", loc="upper left")

plt.savefig("SampleDay-%d.png" % day)
