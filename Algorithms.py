from Divergence import *
from Utils import *
import statistics
import numpy as np


def sdd_r(collections, step=None, alpha=None, metric=kullbackLeiblerDivergence):
    """
    SDD-R算法

    :param collections: 数据群集合。例如：[{1, 1, 2, 2, 3}, {-1, -1, 0}， {0, 1, 1, 2, 2}]
    :param step: 统计直方图时的步长，默认为None（自动计算）
    :param alpha: 估计的错误概率，默认为None（使用3σ阈值）
    :param metric: 统计距离度量函数，默认为kullbackLeiblerDivergence
    :return: 异常的数据群下标。例如上例中应该返回：[1]
    """
    # 计算直方图步长 #
    if step is None:
        # 以第一个数据collection为基准 #
        sample = collections[0]
        sample_sigma = statistics.stdev(sample)
        step = 1.05 * sample_sigma * (len(sample) ** -0.2)

    # 计算reference以及divergence分布 #
    distributions = [histogram(collection, step)[1] for collection in collections]
    reference = blendDistributions(distributions)
    divergences = [metric([dist, reference]) for dist in distributions]

    if alpha is None:
        # 使用3σ阈值 #
        divergences_mu = statistics.mean(divergences)
        divergences_sigma = statistics.stdev(divergences, divergences_mu)
        return [idx for idx in range(len(divergences)) if divergences[idx] > (3 * divergences_sigma - divergences_mu)]
    else:
        # 使用rank #
        order = list(np.argsort(divergences))
        order.reverse()
        return order[:int(alpha * len(collections))]


def sdd_r_rank(collections, step=None, metric=kullbackLeiblerDivergence):
    """
    SDD-R 异常度排序

    :param collections: 数据群集合。例如：[{1, 1, 2, 2, 3}, {-1, -1, 0}， {0, 1, 1, 2, 2}]
    :param step: 统计直方图时的步长，默认为None（自动计算）
    :param metric: 统计距离度量函数，默认为kullbackLeiblerDivergence
    :return: 数据群下标排序，根据异常度从高到低排序
    """
    # 计算直方图步长 #
    if step is None:
        # 以第一个数据collection为基准 #
        sample = collections[0]
        sample_sigma = statistics.stdev(sample)
        step = 1.05 * sample_sigma * (len(sample) ** -0.2)

    # 计算reference以及divergence #
    distributions = [histogram(collection, step)[1] for collection in collections]
    reference = blendDistributions(distributions)
    divergences = [metric([dist, reference]) for dist in distributions]

    # 排序 #
    order = list(np.argsort(divergences))
    order.reverse()
    return order


def sdd_e(evidence_normal, evidence_anomalous, collections, step=None, alpha=None,
          metric=kullbackLeiblerDivergence, dynamic=False):
    """
    SDD-E算法

    :param evidence_normal: 正常数据观察集
    :param evidence_anomalous: 异常数据观察集
    :param alpha: 估计的异常概率，默认为None
    :param collections: 数据群集合（有序的，因为要使得动态更新观察集有意义）。例如：
    [{1, 1, 2, 2, 3}, {-1, -1, 0}， {0, 1, 1, 2, 2}]
    :param step: 统计直方图时的步长，默认为None（自动计算）
    :param metric: 统计距离度量函数，默认为kullbackLeiblerDivergence
    :param dynamic: 是否动态更新观察集（Evidence Set）
    :return: 异常的数据群下标。例如上例中应该返回：[1]
    """
    def _calculate_threshold(reference, distributions_normal, distributions_anomalous, alpha):
        """
        定义根据观察集计算reference和threshold的过程

        :param evidence_normal:
        :param evidence_anomalous:
        :param alpha:
        :return: reference distribution, threshold
        """
        def _check_threshold(un, sn, ua, sa, alpha, t):
            """
            计算阈值判别式。

            :param un:
            :param sn:
            :param ua:
            :param sa:
            :param alpha:
            :param t:
            :return:
            """
            left = alpha * (t - ua) / sa**3 * math.exp(-(t - ua)**2 / (2 * sa**2))
            right = (1 - alpha) * (t - un) / sn**3 * math.exp(-(t - un)**2 / (2 * sn**2))
            return left < right

        divergences_normal = [metric([dist, reference]) for dist in distributions_normal]
        divergences_anomalous = [metric([dist, reference]) for dist in distributions_anomalous]

        mu_normal = statistics.mean(divergences_normal)
        sigma_normal = statistics.stdev(divergences_normal, mu_normal)
        mu_anomalous = statistics.mean(divergences_anomalous)
        sigma_anomalous = statistics.stdev(divergences_anomalous, mu_anomalous)

        if mu_normal > mu_anomalous:
            print("Warning: Assumption Violated: mu_n(%g) >= mu_a(%g)" % (mu_normal, mu_anomalous))
            # 假设失效，退化为使用3σ规则 #
            return mu_normal + sigma_normal * 3

        if sigma_anomalous == 0 or sigma_normal == 0:
            print("Warning: Assumption Violated: sigma_n(%g) or sigma_a(%g) is 0" % (sigma_normal, sigma_anomalous))
            # 特殊情况，退化为使用均值 #
            return (mu_normal + mu_anomalous) / 2

        threshold = None
        if sigma_normal == sigma_anomalous:
            threshold = (mu_normal + mu_anomalous) / 2 + \
                        (sigma_normal ** 2 * math.log((1 - alpha) / alpha) / (mu_anomalous - mu_normal))
        else:
            tmp1 = (sigma_anomalous ** 2) * mu_normal - (sigma_normal ** 2) * mu_anomalous
            delta = (mu_anomalous - mu_normal) ** 2 + 2 * (sigma_anomalous ** 2 - sigma_normal ** 2) * math.log(
                    (1 - alpha) * sigma_anomalous / (alpha * sigma_normal)
            )
            if delta < 0:
                # 方程无解，退化为使用3σ规则 #
                return mu_normal + sigma_normal * 3
            tmp2 = sigma_anomalous * sigma_normal * math.sqrt(delta)
            tmp3 = sigma_anomalous ** 2 - sigma_normal ** 2
            threshold1 = (tmp1 + tmp2) / tmp3
            threshold2 = (tmp1 - tmp2) / tmp3

            t1_is_valid = _check_threshold(mu_normal, sigma_normal, mu_anomalous, sigma_anomalous, alpha, threshold1)
            t2_is_valid = _check_threshold(mu_normal, sigma_normal, mu_anomalous, sigma_anomalous, alpha, threshold2)

            if t1_is_valid:
                if t2_is_valid:
                    print("Warning: Cannot Decide Threshold(Both Valid): un(%g), sn(%g), ua(%g), sa(%g), t1(%g), t2(%g)" %(
                        mu_normal, sigma_normal, mu_anomalous, sigma_anomalous, threshold1,threshold2
                    ))
                else:
                    threshold = threshold1
            else:
                if t2_is_valid:
                    threshold = threshold2
                else:
                    print("Warning: Cannot Decide Threshold(Both Invalid): un(%g), sn(%g), ua(%g), sa(%g), t1(%g), t2(%g)" %(
                        mu_normal, sigma_normal, mu_anomalous, sigma_anomalous, threshold1,threshold2
                    ))
            # 精度误差问题，特殊处理 #
            if threshold is None:
                if mu_normal < threshold1 < mu_anomalous:
                    threshold = threshold1
                elif mu_normal < threshold2 < mu_anomalous:
                    threshold = threshold2
                else:
                    print("Fatal Error Occurs: un(%g), sn(%g), ua(%g), sa(%g), t1(%g), t2(%g)" %(
                        mu_normal, sigma_normal, mu_anomalous, sigma_anomalous, threshold1,threshold2
                    ))
                    return mu_normal + sigma_normal * 3
        return threshold

    # 算法开始 #
    # 计算直方图步长 #
    if step is None:
        # 以第一个数据collection为基准 #
        sample = collections[0]
        sample_sigma = statistics.stdev(sample)
        step = 1.05 * sample_sigma * (len(sample) ** -0.2)
    alpha = 0.5 if alpha is None else alpha

    # 计算reference以及threshold #
    distributions_target = [histogram(collection, step)[1] for collection in collections]
    distributions_normal = [histogram(collection, step)[1] for collection in evidence_normal]
    distributions_anomalous = [histogram(collection, step)[1] for collection in evidence_anomalous]
    reference = blendDistributions(distributions_normal)
    threshold = _calculate_threshold(reference, distributions_normal, distributions_anomalous, alpha)

    if dynamic:
        # 动态算法需要更新Evidence Sets #
        # Evidence Sets更新策略为LRU #
        evidence_normal_offset = 0
        evidence_anomalous_offset = 0
        anomalous_indices = []
        for i in range(len(distributions_target)):
            divergence = metric([distributions_target[i], reference])
            if divergence > threshold:
                # 判定为异常 #
                distributions_anomalous[evidence_anomalous_offset % len(evidence_anomalous)] = distributions_target[i]
                evidence_anomalous_offset += 1
                anomalous_indices.append(i)
            else:
                # 判定不是异常 #
                tmp_indx = evidence_normal_offset % len(evidence_normal)
                old_distribution = distributions_normal[tmp_indx]
                new_distribution = distributions_target[i]
                # size = len(distributions_normal)
                # for x, px in reference.items():
                #     reference[x] = px * size
                # for x, px in old_distribution.items():
                #     reference[x] -= px
                # for x, px in new_distribution.items():
                #     if x in reference:
                #         reference[x] += px
                #     else:
                #         reference[x] = px
                # for x, px in reference.items():
                #     reference[x] = px / size
                distributions_normal[tmp_indx] = new_distribution
                reference = blendDistributions(distributions_normal)
                evidence_normal_offset += 1
            threshold = _calculate_threshold(reference, distributions_normal, distributions_anomalous, alpha)
        return anomalous_indices
    else:
        # 静态算法直接计算divergence并根据threshold过滤 #
        divergences_target = [metric([dist, reference]) for dist in distributions_target]
        return [idx for idx in range(len(divergences_target)) if divergences_target[idx] > threshold]


def sdd_e_rank(evidence_normal, collections, step=None, metric=kullbackLeiblerDivergence):
    """
    SDD-E(static) 异常度排序

    :param evidence_normal: 正常数据观察集
    :param evidence_anomalous: 异常数据观察集
    :param collections: 数据群集合（有序的，因为要使得动态更新观察集有意义）。例如：
    [{1, 1, 2, 2, 3}, {-1, -1, 0}， {0, 1, 1, 2, 2}]
    :param step: 统计直方图时的步长，默认为None（自动计算）
    :param metric: 统计距离度量函数，默认为kullbackLeiblerDivergence
    :return: 数据群下标排序，根据异常度从高到低排序
    """
    # 算法开始 #
    # 计算直方图步长 #
    if step is None:
        # 以第一个数据collection为基准 #
        sample = collections[0]
        sample_sigma = statistics.stdev(sample)
        step = 1.05 * sample_sigma * (len(sample) ** -0.2)

    # 计算reference以及threshold #
    distributions_target = [histogram(collection, step)[1] for collection in collections]
    distributions_normal = [histogram(collection, step)[1] for collection in evidence_normal]
    reference = blendDistributions(distributions_normal)

    # 静态算法直接计算divergence #
    divergences_target = [metric([dist, reference]) for dist in distributions_target]

    # 排序 #
    order = list(np.argsort(divergences_target))
    order.reverse()
    return order


# chi-squared分布在各个自由度下的0.99以及0.95置信区间 #
T99s = [0, 6.635, 9.210, 11.345, 13.277, 15.086, 16.812, 18.475, 20.090, 21.666, 23.209, 24.725, 26.217, 27.688,
        29.141, 30.578, 32.000, 33.409, 34.805, 36.191, 37.566, 38.932, 40.289, 41.638, 42.980, 44.314]
T95s = [0, 3.841, 5.991, 7.815, 9.488, 11.070, 12.592, 14.067, 15.507, 16.919, 18.307, 19.675, 21.026, 22.362,
        23.685, 24.996, 26.296, 27.587, 28.869, 30.144, 31.410, 32.671, 33.924, 35.172, 36.415, 37.652]


def mgof(collections, nbins=len(T99s)-1, c_th=10):
    """
    MGoF算法。

    :param collections: 数据群集合（有序的，因为要使得动态更新观察集有意义）。
    :param nbins: 直方图的子区间的数量，默认为目前可以接受的最大数量（根据T99s和T95s的长度定）
    :param c_th: 分布数量阈值，默认为10
    :return:
    """
    # 先求出数据中的最大最小值 #
    value_max = max(collections[0])
    value_min = min(collections[0])
    for i in range(1, len(collections)):
        value_max = max(value_max, max(collections[i]))
        value_min = min(value_min, min(collections[i]))

    step = (value_max - value_min) / nbins
    T = T95s[nbins]

    # 判断每一个分布是否为异常 #
    dropped, dist = histogram(collections[0], step)
    p = [dist]  # m = len(p)，不用单独设置变量
    c = [1]
    anomalous_indices = []
    for i in range(1, len(collections)):
        collection = collections[i]
        W = len(collection)

        dropped, dist = histogram(collection, step)
        klds = [kullbackLeiblerDivergence([dist, p_i]) for p_i in p]
        kld_min_index = min(range(len(klds)), key=klds.__getitem__)
        kld_min = klds[kld_min_index]

        if (2 * W * kld_min) < T:
            c[kld_min_index] += 1
            if c[kld_min_index] < c_th:
                anomalous_indices.append(i)
        else:
            anomalous_indices.append(i)
            p.append(dist)
            c.append(1)
    return anomalous_indices


if __name__ == '__main__':
    print("Test Algorithms")
    collection_raw_nomal = loadCollectionFromFile('Koubei/RawCorrect.csv')
    collection_raw_centralized = loadCollectionFromFile('Koubei/RawCentralized.csv')
    evidence_normal = collection_raw_nomal[:30]
    evidence_anomalous = collection_raw_centralized[:10]
    abnormal_indices = [51, 63, 91, 94, 114, 162, 166, 173, 178, 194, 208, 233, 250, 255, 256, 318]
    alpha = len(abnormal_indices) / len(collection_raw_nomal)
    collection_input = collection_raw_nomal
    for i in abnormal_indices:
        collection_input[i] = collection_raw_centralized[i]

    print('Test sdd_e static:', sdd_e(
        evidence_normal, evidence_anomalous, collection_input, alpha=None, step=None, metric=kullbackLeiblerDivergence, dynamic=False
    ))
    print('Test sdd_e dynamic:', sdd_e(
        evidence_normal, evidence_anomalous, collection_input, alpha=None, step=None, metric=kullbackLeiblerDivergence, dynamic=True
    ))
