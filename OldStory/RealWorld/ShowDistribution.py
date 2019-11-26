import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import random

# figure = plt.figure(figsize=(8, 4.2), dpi=120)
# plt_cnt = 0
# for day in (5, 113, 287):
#     #figure = plt.figure(figsize=(5, 5), dpi=100)
#     reader = csv.reader(open("Correct/%d.csv" % day, 'r'))
#     freq = {}
#     for i in range(24):
#         freq[i] = 0
#     for row in reader:
#         freq[int(row[2])] += 1
#
#     plt_cnt += 1
#     plt.subplot(1, 3, plt_cnt)
#     plt.bar(list(range(24)), freq.values())
#     plt.title("Day %d" % day)
#     if 2 == plt_cnt:
#         plt.xlabel("Hour", fontsize='x-large')
#     else:
#         plt.xlabel(' ', fontsize='x-large')
#     if 1 == plt_cnt:
#         plt.ylabel("Transaction Volume", fontsize='x-large')
#     #plt.savefig("SaleDistributions-%d.png" % plt_cnt)
#     #figure.savefig("SaleDistributions-%d.png" % plt_cnt)
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

figure = plt.figure(figsize=(8, 4.4), dpi=100)
plt.subplot(1, 2, 1)
plt.bar(list(range(24)), freq1.values(), label="1st Level")
plt.title("1st Level")
plt.xlabel("Time Span", fontsize='x-large')
plt.ylabel("Transaction Volume", fontsize='x-large')
#plt.legend()

plt.subplot(1, 2, 2)
plt.bar(list(range(10)), freq2.values(), label="2st Level")
plt.title("2nd Level")
plt.xlabel("Volume Span", fontsize='x-large')
plt.ylabel("Frequency", fontsize='x-large')
#plt.legend()

plt.savefig("HistogramExample.png")