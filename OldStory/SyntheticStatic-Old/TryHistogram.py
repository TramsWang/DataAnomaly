import csv
import itertools
import Divergence
import statistics
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


f = open("brackets.txt", 'r')
min_val = int(f.readline())
max_val = int(f.readline())
f.close()

dists = []
total_data = []
for i in range(134, 164):
    with open("Inputs/%d.csv" % i, 'r') as f:
        reader = csv.reader(f)
        records = list(int(row[2]) for row in itertools.islice(reader, 0, None))
        distribution = Divergence.histogramNaive(min_val, max_val, records)
        dists += [distribution]
        total_data += records

total_cnt = len(total_data)
sigma = statistics.stdev(total_data)
step = math.pow(total_cnt / 30, -0.2) * sigma * 0.5
num_bins = (max_val - min_val) / step
print(max_val, min_val)
print(total_cnt)
print(sigma)
print("Step: ", step)
print("Num Bins: ", num_bins)
print("Bin Width: ", (max_val - min_val) / 50)

# # Check two examples
# figure = plt.figure(figsize=(1800/300, 600/300), dpi=300)
#
# ifile = open("Inputs/134.csv", 'r')
# ifile_cen = open("InputsCentralized/134.csv", 'r')
# ifile_equ = open("InputsEqualized/134.csv", 'r')
#
# records = list(int(row[2]) for row in itertools.islice(csv.reader(ifile), 0, None))
# records_cen = list(int(row[2]) for row in itertools.islice(csv.reader(ifile_cen), 0, None))
# records_equ = list(int(row[2]) for row in itertools.islice(csv.reader(ifile_equ), 0, None))
#
# for pw in range(10):
#     nbins = 2 ** (pw + 1)
#     step = (max_val - min_val) / nbins
#     distribution = Divergence.getDistribution(math.floor((i - min_val) / step) for i in records)
#     distribution_cen = Divergence.getDistribution(math.floor((i - min_val) / step) for i in records_cen)
#     distribution_equ = Divergence.getDistribution(math.floor((i - min_val) / step) for i in records_equ)
#
#     plt.subplot(131)
#     x = []
#     y = []
#     for i in distribution:
#         x += [i]
#         y += [distribution[i]]
#     plt.bar(x, y, color="red")
#
#     plt.subplot(132)
#     x = []
#     y = []
#     for i in distribution_cen:
#         x += [i]
#         y += [distribution_cen[i]]
#     plt.bar(x, y, color="blue")
#
#     plt.subplot(133)
#     x = []
#     y = []
#     for i in distribution_equ:
#         x += [i]
#         y += [distribution_equ[i]]
#     plt.bar(x, y, color="green")
#
#     plt.savefig("Distribution(nbins=%d).png" % nbins)
#     figure.clear()