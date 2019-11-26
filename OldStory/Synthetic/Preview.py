import csv
import Divergence
import statistics
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

input_dir = "Correct"
input_dir_cen = "Centralized"
input_dir_equ = "Equalized"

# Collecting History
history = []
for i in range(30):
    reader = csv.reader(open("%s/%d.csv" % (input_dir, i), 'r'))
    history += [list(int(row[2]) for row in reader)]

# Emulate Algorithm
jsds = []
jsds_cen = []
jsds_equ = []
jsds2 = []
jsds_cen2 = []
jsds_equ2 = []
for i in range(30, 325):
    # Calculate Step
    tmp = []
    for tmp_data in history:
        tmp += tmp_data
    sigma = statistics.stdev(tmp)
    step = 0.5 * sigma * (statistics.mean(list(len(data) for data in history)) ** -0.2)

    # Calculate evidence distributions and estimated population distribution
    dists = []
    for tmp_data in history:
        dropped, tmp_dist = Divergence.histogram(tmp_data, step)
        dists += [tmp_dist]
    dist_pop = Divergence.blendDistributions(dists)

    # Read and calculate correct, centralized and equalized distribution
    reader = csv.reader(open("%s/%d.csv" % (input_dir, i), 'r'))
    next_data = list((int(row[2]) for row in reader))
    dropped, dist = Divergence.histogram(next_data, step)
    reader = csv.reader(open("%s/%d.csv" % (input_dir_cen, i), 'r'))
    next_data_cen = list((int(row[2]) for row in reader))
    dropped, dist_cen = Divergence.histogram(next_data_cen, step)
    reader = csv.reader(open("%s/%d.csv" % (input_dir_equ, i), 'r'))
    next_data_equ = list((int(row[2]) for row in reader))
    dropped, dist_equ = Divergence.histogram(next_data_equ, step)

    # Calculate JSDs
    jsds += [Divergence.jsd(dist_pop, dist)]
    jsds_cen += [Divergence.jsd(dist_pop, dist_cen)]
    jsds_equ += [Divergence.jsd(dist_pop, dist_equ)]

    ''' Check 2nd order anomalies '''
    # Collect 2nd order data
    span = 600
    history2 = []
    for tmp_data in history:
        tmp_freq, dropped = Divergence.histogram(tmp_data, span)
        history2 += [tmp_freq]

    # Calculate 2nd order step
    tmp = []
    for tmp_data in history2:
        tmp += tmp_data
    sigma2 = statistics.stdev(tmp)
    step2 = 0.5 * sigma2 * (statistics.mean(list(len(data) for data in history2)) ** -0.2)

    # Calculate 2nd order evidence distributions
    dists2 = []
    for data in history2:
        tmp_freq, tmp_dist = Divergence.histogram(data, step2)
        dists2 += [tmp_dist]
    dist_pop2 = Divergence.blendDistributions(dists2)

    # Calculate 2nd order distribution
    next_data2, dropped = Divergence.histogram(next_data, span)
    next_data_cen2, dropped = Divergence.histogram(next_data_cen, span)
    next_data_equ2, dropped = Divergence.histogram(next_data_equ, span)

    # Calculate 2nd order distributions
    dropped, dist2 = Divergence.histogram(next_data2, step2)
    dropped, dist_cen2 = Divergence.histogram(next_data_cen2, step2)
    dropped, dist_equ2 = Divergence.histogram(next_data_equ2, step2)

    # Calculate 2nd order JSDs
    jsds2 += [Divergence.jsd(dist_pop2, dist2)]
    jsds_cen2 += [Divergence.jsd(dist_pop2, dist_cen2)]
    jsds_equ2 += [Divergence.jsd(dist_pop2, dist_equ2)]

    # Move the sliding window
    del history[0]
    history += [next_data]
    print("%d.csv: Step1: %f ;Step2: %f" % (i, step, step2))

# Plot to view
figure = plt.figure(figsize=(1800/300, 1200/300), dpi=300)
plt.subplot(211)
plt.plot(jsds, [0] * len(jsds), 'r.', ms=1, label="Correct")
plt.plot(jsds_cen, [1] * len(jsds_cen), 'b.', ms=1, label="Centralized")
plt.plot(jsds_equ, [-1] * len(jsds_equ), 'g.', ms=1, label="Equalized(Span=%.2f)" % span)
plt.grid()
plt.legend(loc="upper right", fontsize="xx-small")
plt.title("1st Order")

plt.subplot(212)
plt.plot(jsds2, [0] * len(jsds2), 'r.', ms=1, label="Correct")
plt.plot(jsds_cen2, [1] * len(jsds_cen2), 'b.', ms=1, label="Centralized")
plt.plot(jsds_equ2, [-1] * len(jsds_equ2), 'g.', ms=1, label="Equalized")
plt.grid()
plt.legend(loc="upper right", fontsize="xx-small")
plt.title("2nd Order")

plt.savefig("Preview(Span=%.2f).png" % span)

