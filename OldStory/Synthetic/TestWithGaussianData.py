import math
import numpy
import statistics


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
    elif ua <= sol2 <= ub:
        return sol2
    else:
        return ub

alpha = 0.1

f1s = []
falses = []
n = 500

for round in range(n):
    ua = numpy.random.random() * 10
    sa = numpy.random.random() * 5
    ub = numpy.random.random() * 10 + ua
    sb = numpy.random.random() * 5

    total_cnt = 100000
    correct_cnt = int(total_cnt * (1 - alpha))
    correct_recognized = 0
    error_cnt = int(total_cnt * alpha)
    error_recognized = 0

    data = list(numpy.random.normal(ua, sa, correct_cnt))
    data_err = list(numpy.random.normal(ub, sb, error_cnt))

    # 1
    # w = sb
    # w_err = sa

    # 2
    # w = math.sqrt(sb)
    # w_err = math.sqrt(sa)

    # 3
    # w = math.log(sb)
    # w_err = math.log(sa)

    # 4
    # w = math.sqrt(abs(math.log(sb)))
    # w_err = math.sqrt(abs(math.log(sa)))

    # 5
    # w = math.log(math.sqrt(sb))
    # w_err = math.log(math.sqrt(sa))

    # 6
    # w = sb * (1 - alpha)
    # w_err = sa * alpha

    # 7
    # w = sb * math.sqrt(1 - alpha)
    # w_err = sa * math.sqrt(alpha)

    # 8
    # w = sb * math.log(1 - alpha)
    # w_err = sa * math.log(alpha)

    # 9
    # w = sb * math.sqrt(-math.log(1 - alpha))
    # w_err = sa * math.sqrt(-math.log(alpha))

    # 10
    # w = sb * math.log(math.sqrt(1 - alpha))
    # w_err = sa * math.log(math.sqrt(alpha))

    # 11
    # w = math.sqrt(abs(math.log(sb * (1 - alpha))))
    # w_err = math.sqrt(abs(math.log(sa * alpha)))

    # 12
    w = math.log(math.sqrt(sb * (1 - alpha)))
    w_err = math.log(math.sqrt(sa * alpha))

    threshold = (ua * w + ub * w_err) / (w + w_err)

    # 13
    #threshold = linearBalancedThreshold(ua, sa, ub, sb, alpha)
    print("Threshold: %d" % threshold)

    for i in data:
        if i < threshold:
            correct_recognized += 1
    for i in data_err:
        if i > threshold:
            error_recognized += 1

    tp = error_recognized
    fp = correct_cnt - correct_recognized
    tn = correct_recognized
    fn = error_cnt - error_recognized

    if tp == 0:
        f1 = 0
    else:
        pre = tp / (tp + fp)
        rec = tp / (tp + fn)
        f1 = 2 * pre * rec / (pre + rec)
    print("tp=%d, fp=%d, tn=%d, fn=%d, f1=%f\n" % (tp, fp, tn, fn, f1))
    f1s += [f1]
    falses += [fp + fn]

print(statistics.mean(f1s), statistics.mean(falses) / total_cnt)
