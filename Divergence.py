import math


def getDistribution(sample):
    """
    计算样本中各个值的频率。

    :param sample: 数值数组，如：[1, 2, 1, 0.5, -5]
    :return: 两个map：
        1) 各个值的频次映射，结构为：<value, frequency>，如：{-5:1, 0.5:1, 1:2, 2: 1}
        2) 各个值的频率映射，结构为：<value, frequency>，如：{-5:0.2, 0.5:0.2, 1:0.4, 2: 0.2}
    """
    counts = {}
    cnt = 0
    for obj in sample:
        cnt += 1
        if obj in counts:
            counts[obj] += 1
        else:
            counts[obj] = 1
    frequencies = {}
    for value, cnt in counts.items():
        frequencies[value] = cnt / len(sample)
    return counts, frequencies


def blendDistributions(distributions):
    """
    取一系列分布的平均分布。

    :param distributions: 分布数组，每一个分布都是<value, probability>的map。其中value的类型都为数值。如：
    [{1:0.4, -1:0.6}, {-5:0.2, 0.5:0.2, 1:0.4, 2: 0.2}, {0:0.3, 1:0.3, 2:0.4}]
    :return: 分布的平均。结构为：<value, probability>如：{1:0.367, -1:0.2, -5:0.067,
     0.5:0.067, 2:0.2, 0:0.1, }
    """
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


def kullbackLeiblerDivergence(distributions):
    """
    计算两个分布的Kullback-Leibler Divergence。两个分布的结构都是<value, probability>。在这里
    原始定义需要被扩充以适应当P和Q的定义域不满足原始定义需求的情况。即，只考虑x∈(X_P ∩ X_Q)

    例如：{0:0.3, 1:0.3, 2:0.4}, {-5:0.2, 0.5:0.2, 1:0.4, 2:0.2}，计算结果为：0.2755

    :param distributions: 需要求统计距离的两个结构数组，对应到定义上，P=distribution[0], Q=distribution[1]
    :return:
    """
    p = distributions[0]
    q = distributions[1]
    divergence = 0.0
    for value, probability in q.items():
        if 0 != probability:
            p_x = p.get(value)
            if (p_x is not None) and (p_x != 0):
                divergence += p_x * math.log2(p_x / probability)
    return divergence


def jensenShannonDivergence(distributions):
    """
    计算多个分布的Jenson-Shannon Divergence。

    :param distributions: 分布列表。如：[{1:0.4, -1:0.6}, {-5:0.2, 0.5:0.2, 1:0.4,
     2: 0.2}, {0:0.3, 1:0.3, 2:0.4}]
    :return:
    """
    distribution_m = blendDistributions(distributions)
    divergence = 0.0
    for distribution in distributions:
        divergence += kullbackLeiblerDivergence([distribution, distribution_m])
    return divergence / len(distributions)


def bhattacharyyaDistance(distributions):
    """
    计算两个分布的Bhattacharyya Distance。两个分布的结构都是<value, probability>。在这里
    原始定义需要被扩充以适应当P和Q的定义域不满足原始定义需求的情况。即，只考虑x∈(X_P ∩ X_Q)

    例如：{0:0.3, 1:0.3, 2:0.4}, {-5:0.2, 0.5:0.2, 1:0.4, 2:0.2}，计算结果为：0.4632

    :param distributions: 需要求统计距离的两个结构数组，对应到定义上，P=distribution[0], Q=distribution[1]
    :return:
    """
    p = distributions[0]
    q = distributions[1]
    distance = 0.0
    for value, probability in p.items():
        q_x = q.get(value)
        if q_x is not None:
            distance += math.sqrt(probability * q_x)
    # 到这一步为止，distance = 0等价于两个分布定义域不相交 #
    # 如果两个定义域不相交则给一个巨大的值 #
    return -math.log(distance) if distance != 0 else 99999.0


def hellingerDistance(distributions):
    """
    计算两个分布的Hellinger Distance。两个分布的结构都是<value, probability>。

    例如：{0:0.3, 1:0.3, 2:0.4}, {-5:0.2, 0.5:0.2, 1:0.4, 2:0.2}，计算结果为：0.6089

    :param distributions: 需要求统计距离的两个结构数组，对应到定义上，P=distribution[0], Q=distribution[1]
    :return:
    """
    p = distributions[0]
    q = distributions[1]
    distance = 0.0

    for value, probability in p.items():
        q_x = q.get(value)
        if q_x is None:
            distance += probability
        else:
            distance += (math.sqrt(probability) - math.sqrt(q_x)) ** 2
    for value, probability in q.items():
        if value not in p:
            distance += probability
    return math.sqrt(distance) / math.sqrt(2)


def kolmogorovSmirnovStatistic(distributions):
    """
    计算两个分布的Bhattacharyya Distance。两个分布的结构都是<value, probability>。

    例如：{0:0.3, 1:0.3, 2:0.4}, {-5:0.2, 0.5:0.2, 1:0.4, 2:0.2}，计算结果为：0.2

    :param distributions: 需要求统计距离的两个结构数组，对应到定义上，P=distribution[0], Q=distribution[1]
    :return:
    """
    p = distributions[0]
    q = distributions[1]
    distance = 0.0

    xs = sorted(set(p.keys()).union(q.keys()))
    cdf_p = 0
    cdf_q = 0
    for x in xs:
        p_x = p.get(x)
        q_x = q.get(x)
        cdf_p += 0 if p_x is None else p_x
        cdf_q += 0 if q_x is None else q_x
        distance = max(distance, abs(cdf_p - cdf_q))

    return distance


def histogram(sample, step):
    """
    计算样本的直方图。

    :param sample: 数值数组，如：[1, 2, 1, 0.5, -5]
    :param step: 直方图统计的步长
    :return: 两个map：
        1) 各个值的频次映射，如：step=2时为{0:3, 1:1, -3:1}
        2) 各个值的频率映射，如：step=2时为{0:0.6, 1:0.2, -3:0.2}
    """
    return getDistribution([math.floor(i / step) for i in sample])


if __name__ == '__main__':
    print("Tests(Examples): ")
    print("Test 'getDistribution': ", getDistribution([1, 2, 1, 0.5, -5]))
    print("Test 'blendDistribution': ", blendDistributions([
        {1: 0.4, -1: 0.6},
        {-5: 0.2, 0.5: 0.2, 1: 0.4, 2: 0.2},
        {0: 0.3, 1: 0.3, 2: 0.4}
    ]))
    print("Test 'kullbackLeiblerDivergence'", kullbackLeiblerDivergence([
        {0: 0.3, 1: 0.3, 2: 0.4},
        {-5: 0.2, 0.5: 0.2, 1: 0.4, 2: 0.2}
    ]))
    print("Test 'jensenShannonDivergence'", jensenShannonDivergence([
        {1: 0.4, -1: 0.6},
        {-5: 0.2, 0.5: 0.2, 1: 0.4, 2: 0.2},
        {0: 0.3, 1: 0.3, 2: 0.4}
    ]))
    print("Test 'bhattacharyyaDistance'", bhattacharyyaDistance([
        {0: 0.3, 1: 0.3, 2: 0.4},
        {-5: 0.2, 0.5: 0.2, 1: 0.4, 2: 0.2}
    ]))
    print("Test 'hellingerDistance'", hellingerDistance([
        {0: 0.3, 1: 0.3, 2: 0.4},
        {-5: 0.2, 0.5: 0.2, 1: 0.4, 2: 0.2}
    ]))
    print("Test 'kolmogorovSmirnovStatistic'", kolmogorovSmirnovStatistic([
        {0: 0.3, 1: 0.3, 2: 0.4},
        {-5: 0.2, 0.5: 0.2, 1: 0.4, 2: 0.2}
    ]))
    print("Test 'histogram'", histogram([1, 2, 1, 0.5, -5], 2))

    print("Test JSD")
    print(jensenShannonDivergence([
        {1: 0.3333333, 2: 0.3333333, 3: 0.3333333},
        {1: 0.1666667, 2: 0.3333333, 3: 0.5}
    ]))
    print(jensenShannonDivergence([
        {1: 0.3333333, 2: 0.3333333, 3: 0.3333333},
        {1: 0.3333333, 2: 0.3333333, 3: 0.3333333},
        {1: 0.3333333, 2: 0.3333333, 3: 0.3333333},
        {1: 0.1666667, 2: 0.3333333, 3: 0.5}
    ]))
