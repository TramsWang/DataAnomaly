import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random

# figure = plt.figure(figsize=(9, 3), dpi=100)
# plt_cnt = 0
# for day in (5, 113, 287):
#     reader = csv.reader(open("Correct/%d.csv" % day, 'r'))
#     freq = {}
#     for i in range(24):
#         freq[i] = 0
#     for row in reader:
#         freq[int(row[2])] += 1
#
#     plt_cnt += 1
#     plt.subplot(1, 3, plt_cnt)
#     plt.bar(list(range(24)), freq.values(), label="day %d" % day)
#     plt.legend(loc="upper left")
#
# plt.savefig("SaleDistributions.png")

reader = csv.reader(open("Correct/5.csv", 'r'))
freq1 = {}
for i in range(24):
    freq1[i] = 0
for row in reader:
    freq1[int(row[2])] += 1

freq2 = {}
for i in range(10):
    freq2[i] = 0
for i in freq1.keys():
    bsk = int(freq1[i] / 20)
    freq2[bsk] += 1

figure = plt.figure(figsize=(8, 4), dpi=100)
plt.subplot(1, 2, 1)
plt.bar(list(range(24)), freq1.values(), label="1st Level")
plt.legend()

plt.subplot(1, 2, 2)
plt.bar(list(range(10)), freq2.values(), label="2st Level")
plt.legend()

plt.savefig("HistogramExample.png")