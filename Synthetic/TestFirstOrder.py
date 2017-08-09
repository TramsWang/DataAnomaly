import csv
import Divergence
import statistics
import random
import scipy.stats as stats
import sys


input_dir = "Correct"
input_dir_err = "Centralized"

error_rate = 0.1
sigma_coefficient = 4  # Don't think about this now
#threshold = 0.02

print("\nTest Centralized Cheating...")
# Collecting History
history = []
for i in range(30):
    reader = csv.reader(open("%s/%d.csv" % (input_dir, i), 'r'))
    history += [list(int(row[2]) for row in reader)]

history_err = []
for i in range(20, 30):
    reader = csv.reader(open("%s/%d.csv" % (input_dir_err, i), 'r'))
    history_err += [list(int(row[2]) for row in reader)]

# Run algorithm with centralized cheating data
jsds = []
jsds_cen = []
jsds2 = []
jsds_cen2 = []
correct_cnt = 0
correct_recognized = 0
correct_recognized2 = 0
centralized_cnt = 0
centralized_recognized = 0
centralized_recognized2 = 0
for i in range(30, 325):
    # Calculate Step
    tmp = []
    for data in history:
        tmp += data
    sigma = statistics.stdev(tmp)
    step = 0.5 * sigma * (statistics.mean(list(len(data) for data in history)) ** -0.2)

    # Calculate evidence distributions and estimated population distribution
    dists = []
    freqs = []
    for data in history:
        tmp_freq, tmp_dist = Divergence.histogram(data, step)
        freqs += [tmp_freq]
        dists += [tmp_dist]
    dist_pop = Divergence.blendDistributions(dists)
    jsd_hisotry = []
    for tmp_dist in dists:
        jsd_hisotry += [Divergence.jsd(dist_pop, tmp_dist)]
    jsd_mean = statistics.mean(jsd_hisotry)
    jsd_sigma = statistics.stdev(jsd_hisotry)

    jsd_hisotry_err = []
    for data in history_err:
        dropped, tmp_dist = Divergence.histogram(data, step)
        jsd_hisotry_err += [Divergence.jsd(dist_pop, tmp_dist)]
    jsd_mean_err = statistics.mean(jsd_hisotry_err)
    jsd_sigma_err = statistics.stdev(jsd_hisotry_err)

    threshold = (jsd_mean * jsd_sigma_err + jsd_mean_err * jsd_sigma) / (jsd_sigma_err + jsd_sigma)

    # Read and calculate correct, centralized and equalized distribution
    reader = csv.reader(open("%s/%d.csv" % (input_dir, i), 'r'))
    new_data = list((int(row[2]) for row in reader))
    freq, dist = Divergence.histogram(new_data, step)
    reader = csv.reader(open("%s/%d.csv" % (input_dir_err, i), 'r'))
    new_data_cen = list((int(row[2]) for row in reader))
    freq_cen, dist_cen = Divergence.histogram(new_data_cen, step)

    # # Collect 2nd order evidence
    # history2 = []
    # for tmp_freq in freqs:
    #     history2 += [list(tmp_freq.values())]

    # # Calculate 2nd order step
    # tmp = []
    # for data in history2:
    #     tmp += data
    # sigma2 = statistics.stdev(tmp)
    # step2 = 0.5 * sigma2 * (statistics.mean(list(len(data) for data in history2)) ** -0.2)
    #
    # # Calculate 2nd order evidence distributions
    # dists2 = []
    # for data in history2:
    #     tmp_freq, tmp_dist = Divergence.histogram(data, step2)
    #     dists2 += [tmp_dist]
    # dist_pop2 = Divergence.blendDistributions(dists2)
    # jsd_hisotry2 = []
    # for tmp_dist in dists2:
    #     jsd_hisotry2 += [Divergence.jsd(dist_pop2, tmp_dist)]
    # jsd_mean2 = statistics.mean(jsd_hisotry2)
    # jsd_sigma2 = statistics.stdev(jsd_hisotry2)
    #
    # # Calculate 2nd order distributions
    # new_data2 = list(freq.values())
    # freq2, dist2 = Divergence.histogram(new_data2, step2)
    # new_data_cen2 = list(freq_cen.values())
    # freq_cen2, dist_cen2 = Divergence.histogram(new_data_cen2, step2)

    # Choose to be anomaly or not
    if random.uniform(0.0, 1.0) < error_rate:
        # Check anomaly data
        centralized_cnt += 1
        tmp_jsd = Divergence.jsd(dist_pop, dist_cen)
        jsds_cen += [tmp_jsd]
        prob_dens = stats.norm.pdf(tmp_jsd, jsd_mean, jsd_sigma)
        sys.stderr.write("Erroneous PD: %g(jsd: %g[%g, %g])\n"
                         % (prob_dens, tmp_jsd, jsd_mean - sigma_coefficient * jsd_sigma,
                            jsd_mean + sigma_coefficient * jsd_sigma))
        sys.stderr.flush()
        # tmp_jsd2 = Divergence.jsd(dist_pop2, dist_cen2)
        # jsds_cen2 += [tmp_jsd2]

        #if (tmp_jsd >= (jsd_mean + sigma_coefficient * jsd_sigma)) or \
        #        (tmp_jsd <= (jsd_mean - sigma_coefficient * jsd_sigma)):
        if tmp_jsd > threshold:
            centralized_recognized += 1
            del history_err[0]
            history_err += [new_data_cen]
        else:
            # Slide window forward
            del history[0]
            history += [new_data_cen]

        # if (tmp_jsd2 >= (jsd_mean2 + 3 * jsd_sigma2)) or (tmp_jsd2 <= (jsd_mean2 - 3 * jsd_sigma2)):
        #     centralized_recognized2 += 1
        # else:
        #     # Slide window forward
        #     del history2[0]
        #     history2 += [new_data_cen2]

    else:
        # Check correct data
        correct_cnt += 1
        tmp_jsd = Divergence.jsd(dist_pop, dist)
        jsds += [tmp_jsd]
        prob_dens = stats.norm.pdf(tmp_jsd, jsd_mean, jsd_sigma)
        print("Correct PD: %g(jsd: %g)" % (prob_dens, tmp_jsd))
        # tmp_jsd2 = Divergence.jsd(dist_pop2, dist2)
        # jsds2 += [tmp_jsd2]

        #if (tmp_jsd <= (jsd_mean + sigma_coefficient * jsd_sigma)) and \
        #        (tmp_jsd >= (jsd_mean - sigma_coefficient * jsd_sigma)):
        if prob_dens >= threshold:
            # Slide window forward
            correct_recognized += 1
            del history[0]
            history += [new_data]
        else:
            del history_err[0]
            history_err += [new_data]

        # if (tmp_jsd2 <= (jsd_mean2 + 3 * jsd_sigma2)) and (tmp_jsd >= (jsd_mean2 - 3 * jsd_sigma2)):
        #     # Slide window forward
        #     correct_recognized2 += 1
        #     del history2[0]
        #     history2 += [new_data2]

    #th = stats.norm.pdf(jsd_mean + sigma_coefficient * jsd_sigma, jsd_mean, jsd_sigma)
    thpd = stats.norm.pdf(threshold, jsd_mean, jsd_sigma)
    print("Test File: %d.csv(%d/325) Threshold: %g(jsd: %g)(%d sigma)" % (i, i, thpd, threshold, sigma_coefficient))

# Record results
print("\nCorrect: %f(%d/%d); %s: %f(%d/%d)\n" %
      (100 * correct_recognized / correct_cnt, correct_recognized, correct_cnt, input_dir_err,
       100 * centralized_recognized / centralized_cnt, centralized_recognized, centralized_cnt))

