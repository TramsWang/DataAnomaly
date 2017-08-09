import csv
import Divergence
import statistics
import random
import scipy.stats as stats


input_dir = "Correct"
input_dir_err = "Equalized"

error_rate = 0.1
sigma_coefficient = 3  # Don't think about this now
time_span = 600

print("\nTest Centralized Cheating...")
# Collecting History
history = []
for i in range(30):
    reader = csv.reader(open("%s/%d.csv" % (input_dir, i), 'r'))
    tmp_freq, dropped = Divergence.histogram(list(int(row[2]) for row in reader), time_span)
    history += [list(tmp_freq.values())]

# Run algorithm with centralized cheating data
jsds = []
jsds_cen = []
correct_cnt = 0
correct_recognized = 0
centralized_cnt = 0
centralized_recognized = 0
for i in range(30, 325):
    # Calculate Step
    tmp = []
    for data in history:
        tmp += data
    sigma = statistics.stdev(tmp)
    step = 0.5 * sigma * (statistics.mean(list(len(data) for data in history)) ** -0.2)

    # Calculate evidence distributions and estimated population distribution
    dists = []
    for data in history:
        dropped, tmp_dist = Divergence.histogram(data, step)
        dists += [tmp_dist]
    dist_pop = Divergence.blendDistributions(dists)
    jsd_hisotry = []
    for tmp_dist in dists:
        jsd_hisotry += [Divergence.jsd(dist_pop, tmp_dist)]
    jsd_mean = statistics.mean(jsd_hisotry)
    jsd_sigma = statistics.stdev(jsd_hisotry)

    # Read and calculate correct, centralized and equalized distribution
    reader = csv.reader(open("%s/%d.csv" % (input_dir, i), 'r'))
    freq, dropped = Divergence.histogram(list((int(row[2]) for row in reader)), time_span)
    new_data = list(freq.values())
    dropped, dist = Divergence.histogram(new_data, step)
    reader = csv.reader(open("%s/%d.csv" % (input_dir_err, i), 'r'))
    freq_cen, dropped = Divergence.histogram(list((int(row[2]) for row in reader)), time_span)
    new_data_cen = list(freq_cen.values())
    dropped, dist_cen = Divergence.histogram(new_data_cen, step)

    # Choose to be anomaly or not
    if random.uniform(0.0, 1.0) < error_rate:
        # Check anomaly data
        centralized_cnt += 1
        tmp_jsd = Divergence.jsd(dist_pop, dist_cen)
        jsds_cen += [tmp_jsd]

        if (tmp_jsd >= (jsd_mean + sigma_coefficient * jsd_sigma)) or \
                (tmp_jsd <= (jsd_mean - sigma_coefficient * jsd_sigma)):
            centralized_recognized += 1
        else:
            # Slide window forward
            del history[0]
            history += [new_data_cen]

    else:
        # Check correct data
        correct_cnt += 1
        tmp_jsd = Divergence.jsd(dist_pop, dist)
        jsds += [tmp_jsd]

        if (tmp_jsd <= (jsd_mean + sigma_coefficient * jsd_sigma)) and \
                (tmp_jsd >= (jsd_mean - sigma_coefficient * jsd_sigma)):
            # Slide window forward
            correct_recognized += 1
            del history[0]
            history += [new_data]

    threshold = stats.norm.pdf(jsd_mean + sigma_coefficient * jsd_sigma, jsd_mean, jsd_sigma)
    print("Test File: %d.csv(%d/325) Threshold: %g(%f sigma)" % (i, i, threshold, sigma_coefficient))

# Record results
print("\nCorrect: %f(%d/%d); Centralized: %f(%d/%d)\n" %
      (100 * correct_recognized / correct_cnt, correct_recognized, correct_cnt,
       100 * centralized_recognized / centralized_cnt, centralized_recognized, centralized_cnt))
