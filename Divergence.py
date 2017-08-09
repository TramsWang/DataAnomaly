import math


def getDistribution(sample):
    frequency = {}
    cnt = 0
    for obj in sample:
        cnt += 1
        if obj in frequency:
            frequency[obj] += 1
        else:
            frequency[obj] = 1
    distribution = {}
    for i in frequency:
        distribution[i] = frequency[i] / cnt
    return frequency, distribution


def blendDistributions(distributions):
    total = {}
    for dist in distributions:
        for i in dist:
            if i in total:
                total[i] += dist[i]
            else:
                total[i] = dist[i]

    for i in total:
        total[i] /= len(distributions)
    return total


def jsd(p, q):
    total = blendDistributions([p, q])

    d = 0.0
    for i in p:
        d += p[i] * math.log(p[i] / total[i])
    for i in q:
        d += q[i] * math.log(q[i] / total[i])
    d /= 2
    return d


def histogram(sequence, step):
    return getDistribution(math.floor(i / step) for i in sequence)


def histogramNaive(min_val, max_val, sequence, nbins=250):
    step = (max_val - min_val) / nbins
    return getDistribution(math.floor((i - min_val) / step) for i in sequence)
