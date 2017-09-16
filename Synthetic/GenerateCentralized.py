import csv
import itertools
import os
import numpy
import Divergence
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ratio = 0.5

input_dir = "Correct"
output_dir = "Centralized(%.1f)" % (1 + ratio)
d = os.path.abspath(output_dir)
if not os.path.exists(d):
    os.makedirs(d)

for file in os.listdir(input_dir):
    print("Processing: ", file)
    with open("%s/%s" % (input_dir, file), 'r') as ifile:
        with open("%s/%s" % (output_dir, file), 'w') as ofile:
            cnt = 0
            for line in ifile:
                cnt += 1
                ofile.write(line)
            #num_new = numpy.random.randint(int(cnt * 1.5), int(cnt * 2.0))
            num_new = int(cnt * ratio)
            center = numpy.random.randint(10, 21)
            for item in numpy.random.normal(center * 3600, 1.5 * 3600, num_new):
                if (item >= (7 * 3600)) and (item < 24 * 3600):
                    ofile.write("921013,1629,%d\n" % int(item))

# # Check two examples
# f = open("brackets.txt", 'r')
# min_val = int(f.readline())
# max_val = int(f.readline())
# f.close()
#
# figure = plt.figure(figsize=(1400/300, 1400/300), dpi=300)
# with open("%s/134.csv" % input_dir, 'r') as f:
#     reader = csv.reader(f)
#     records = (int(row[2]) for row in itertools.islice(reader, 0, None))
#     distribution = Divergence.histogramNaive(min_val, max_val, records)
#     x = []
#     y = []
#     for i in distribution:
#         x += [i]
#         y += [distribution[i]]
#     plt.bar(x, y, color="red")
#     plt.savefig("Sample.png")
#     figure.clear()
#
# with open("%s/134.csv" % output_dir, 'r') as f:
#     reader = csv.reader(f)
#     records = (int(row[2]) for row in itertools.islice(reader, 0, None))
#     distribution = Divergence.histogramNaive(min_val, max_val, records)
#     x = []
#     y = []
#     for i in distribution:
#         x += [i]
#         y += [distribution[i]]
#     plt.bar(x, y, color="blue")
#     plt.savefig("SampleCentralized.png")
#     figure.clear()
