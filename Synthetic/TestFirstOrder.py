import csv
import Divergence
import statistics
import random
import scipy.stats as stats
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import math


def linearBalancedThreshold(ua, sa, ub, sb, alpha):
    A = sb * sb - sa * sa
    B = -2 * (ua * sb * sb - ub * sa * sa)
    C = ua * ua * sb * sb - ub * ub * sa * sa - 2 * sa * sa * sb * sb * math.log(((1 - alpha) * sb) / (alpha * sa))
    D = B * B - 4 * A * C
    if D < 0:
        return ub
    sol1 = (-B + math.sqrt(D)) / (2 * A)
    sol2 = (-B - math.sqrt(D)) / (2 * A)
    # if ua <= sol1 <= ub:
    #     return sol1
    # elif ua <= sol2 <= ub:
    #     return sol2
    # else:
    #     return (ua * sb + ub * sa) / (sa + sb)
    if ua <= sol1 <= ub:
        return sol1
    else:
        return sol2

input_dir = "Correct"
input_dir_err = "Centralized(1.2)"

error_rate = 0.5

print("\nTest %s Cheating..." % input_dir_err)
# Collecting History
evidence = []
for i in range(30):
    reader = csv.reader(open("%s/%d.csv" % (input_dir, i), 'r'))
    evidence += [list(int(row[2]) for row in reader)]

evidence_err = []
for i in range(30 - max(10, int(30 * error_rate)), 30):
    reader = csv.reader(open("%s/%d.csv" % (input_dir_err, i), 'r'))
    evidence_err += [list(int(row[2]) for row in reader)]

# Run algorithm with cheating data
jsd_history = []
jsd_record = {"evidence":[], "evidence_err":[], "correct":-1, "error":-1}
correct_cnt = 0
correct_recognized = 0
error_cnt = 0
error_recognized = 0
for i in range(30, 325):
    # Calculate Step
    tmp = []
    for data in evidence:
        tmp += data
    sigma = statistics.stdev(tmp)
    step = 0.5 * sigma * ((len(tmp) / len(evidence)) ** -0.2)

    # Calculate evidence distributions and estimated population distribution
    dists = []
    for data in evidence:
        dropped, tmp_dist = Divergence.histogram(data, step)
        dists += [tmp_dist]
    dist_pop = Divergence.blendDistributions(dists)
    jsd_evidence = []
    for tmp_dist in dists:
        jsd_evidence += [Divergence.jsd(dist_pop, tmp_dist)]
    jsd_mean = statistics.mean(jsd_evidence)
    jsd_sigma = statistics.stdev(jsd_evidence)

    jsd_evidence_err = []
    for data in evidence_err:
        dropped, tmp_dist = Divergence.histogram(data, step)
        jsd_evidence_err += [Divergence.jsd(dist_pop, tmp_dist)]
    jsd_mean_err = statistics.mean(jsd_evidence_err)
    jsd_sigma_err = statistics.stdev(jsd_evidence_err)

    # w = jsd_sigma_err * math.sqrt(-math.log(1 - error_rate))
    # w_err = jsd_sigma * math.sqrt(-math.log(error_rate))
    # threshold = (jsd_mean * w + jsd_mean_err * w_err) / (w + w_err)
    threshold = 0.01
    #print("Test File: %d.csv(%d/325) Threshold jsd: %g(PD: %g)"
    #      % (i, i, threshold, stats.norm.pdf(threshold, jsd_mean, jsd_sigma)))
    ch = '-'
    if jsd_mean <= threshold <= jsd_mean_err:
        t = (jsd_mean * jsd_sigma_err + jsd_mean_err * jsd_sigma) / (jsd_sigma_err + jsd_sigma)
        if threshold < t:
            ch = '<'
        else:
            ch = '>'
    else:
        ch = 'X'
    print("Test File: %d.csv(%d/325) Threshold jsd: %g(PD: %g) %s"
          % (i, i, threshold, stats.norm.pdf(threshold, jsd_mean, jsd_sigma), ch))
    jsd_record["evidence"] = list(jsd_evidence)
    jsd_record["evidence_err"] = list(jsd_evidence_err)
    jsd_record["threshold"] = threshold

    # Choose to be anomaly or not
    if random.uniform(0.0, 1.0) < error_rate:
        # Check anomaly data
        error_cnt += 1
        reader = csv.reader(open("%s/%d.csv" % (input_dir_err, i), 'r'))
        new_data_err = list((int(row[2]) for row in reader))
        dropped, dist_err = Divergence.histogram(new_data_err, step)
        tmp_jsd = Divergence.jsd(dist_pop, dist_err)
        sys.stderr.write("Erroneous jsd: %g\n" % tmp_jsd)
        sys.stderr.flush()

        # Slide window forward
        if tmp_jsd > threshold:
            error_recognized += 1
            del evidence_err[0]
            evidence_err += [new_data_err]
            jsd_record["error"] = tmp_jsd
            jsd_record["correct"] = -1
        else:
            del evidence[0]
            evidence += [new_data_err]
            jsd_record["error"] = -1
            jsd_record["correct"] = tmp_jsd
    else:
        # Check correct data
        correct_cnt += 1
        reader = csv.reader(open("%s/%d.csv" % (input_dir, i), 'r'))
        new_data = list((int(row[2]) for row in reader))
        dropped, dist = Divergence.histogram(new_data, step)
        tmp_jsd = Divergence.jsd(dist_pop, dist)
        print("Correct jsd: %g" % tmp_jsd)

        if tmp_jsd <= threshold:
            # Slide window forward
            correct_recognized += 1
            del evidence[0]
            evidence += [new_data]
            jsd_record["error"] = -1
            jsd_record["correct"] = tmp_jsd
        else:
            del evidence_err[0]
            evidence_err += [new_data]
            jsd_record["error"] = tmp_jsd
            jsd_record["correct"] = -1
    jsd_history += [dict(jsd_record)]

# Record results
try:
    print("\nCorrect: %f(%d/%d); %s: %f(%d/%d)\n" %
      (100 * correct_recognized / correct_cnt, correct_recognized, correct_cnt, input_dir_err,
       100 * error_recognized / error_cnt, error_recognized, error_cnt))
except ZeroDivisionError as e:
    print(e)

tp = error_recognized
fp = correct_cnt - correct_recognized
tn = correct_recognized
fn = error_cnt - error_recognized

# pre = tp / (tp + fp)
# rec = tp / (tp + fn)
# f1 = 2 * pre * rec / (pre + rec)
print("tp=%d, fp=%d, tn=%d, fn=%d, f1=%f\n" % (tp, fp, tn, fn, 0))

# Show JSD History
# figure = plt.figure(figsize=(6000/300, 3000/300), dpi=300)
# plt.axis("off")
# for i in range(len(jsd_history)):
#     record = jsd_history[i]
#     plt.plot([i] * len(record["evidence"]), record["evidence"], 'r.', ms=0.5)
#     plt.plot([i] * len(record["evidence_err"]), record["evidence_err"], 'b.', ms=0.5)
#     plt.plot(i, record["threshold"], 'gx', ms=3)
#     if record["correct"] == -1:
#         plt.plot(i, record["error"], 'bx', ms=3)
#     else:
#         plt.plot(i, record["correct"], 'rx', ms=3)
# figure.savefig("TestFirstOrder.png")
