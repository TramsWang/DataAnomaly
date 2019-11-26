from typing import List

from Utils import *
from Divergence import *
from Algorithms import *
import numpy as np
import statistics
import time


EXP_DUPLICATE = 5


def testPerformanceOnKoubei():
    # 加载数据 #
    correct_data_raw = loadCollectionFromFile("Koubei/RawCorrect.csv")
    centralized_data_raw = loadCollectionFromFile("Koubei/RawCentralized.csv")
    equalized_data_raw = loadCollectionFromFile("Koubei/RawEqualized.csv")

    correct_data_syn = loadCollectionFromFile("Koubei/SynCorrect.csv")
    centralized_data_syn = loadCollectionFromFile("Koubei/SynCentralized.csv")
    equalized_data_syn = loadCollectionFromFile("Koubei/SynEqualized.csv")

    # 设置参数 #
    alpha = 0.1
    num_anomalies = int(alpha * len(correct_data_raw))
    anomaly_indices_array = [
        sorted(np.random.choice(range(len(correct_data_raw)), num_anomalies, replace=False)) for _ in range(EXP_DUPLICATE)
    ]
    print("Anomalies:")
    for i in range(EXP_DUPLICATE):
        print(anomaly_indices_array[i])

    sample = correct_data_syn[0]
    sample_sigma = statistics.stdev(sample)
    level1_step_syn = 1.05 * sample_sigma * (len(sample) ** -0.2)

    evidence_normal_raw = correct_data_raw[:30]
    evidence_centralized_raw = centralized_data_raw[:10]
    evidence_equalized_raw = equalized_data_raw[:10]
    evidence_normal_raw_level2 = [histogram(collection, 1)[0].values() for collection in evidence_normal_raw]
    evidence_centralized_raw_level2 = [histogram(collection, 1)[0].values() for collection in evidence_centralized_raw]
    evidence_equalized_raw_level2 = [histogram(collection, 1)[0].values() for collection in evidence_equalized_raw]

    evidence_normal_syn = correct_data_syn[:30]
    evidence_centralized_syn = centralized_data_syn[:10]
    evidence_equalized_syn = equalized_data_syn[:10]
    evidence_normal_syn_level2 = [histogram(collection, level1_step_syn)[0].values() for collection in evidence_normal_syn]
    evidence_centralized_syn_level2 = [histogram(collection, level1_step_syn)[0].values() for collection in evidence_centralized_syn]
    evidence_equalized_syn_level2 = [histogram(collection, level1_step_syn)[0].values() for collection in evidence_equalized_syn]

    # 分组进行实验 #
    for i in range(EXP_DUPLICATE):
        print("---------------[DUP %d]---------------------" % i)
        anomaly_indices = anomaly_indices_array[i]

        # 构造输入数据 #
        input_raw_with_centralized = correct_data_raw.copy()
        input_raw_with_equalized = correct_data_raw.copy()
        input_syn_with_centralized = correct_data_syn.copy()
        input_syn_with_equalized = correct_data_syn.copy()
        for idx in anomaly_indices:
            input_raw_with_centralized[idx] = centralized_data_raw[idx]
            input_raw_with_equalized[idx] = equalized_data_raw[idx]
            input_syn_with_centralized[idx] = centralized_data_syn[idx]
            input_syn_with_equalized[idx] = equalized_data_syn[idx]
        input_raw_with_centralized_level2 = [histogram(collection, 1)[0].values() for collection in input_raw_with_centralized]
        input_raw_with_equalized_level2 = [histogram(collection, 1)[0].values() for collection in input_raw_with_equalized]
        input_syn_with_centralized_level2 = [histogram(collection, level1_step_syn)[0].values() for collection in input_syn_with_centralized]
        input_syn_with_equalized_level2 = [histogram(collection, level1_step_syn)[0].values() for collection in input_syn_with_equalized]

        # 统计实验结果(SDD-R) #
        print(">>> SDD-R <<<")
        print("[Test on RAW]")
        time_start = time.time()
        results = sdd_r(input_raw_with_centralized, step=1, alpha=None, metric=jensenShannonDivergence)
        time_stop = time.time()
        print("1st Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_r(input_raw_with_equalized, step=1, alpha=None, metric=jensenShannonDivergence)
        time_stop = time.time()
        print("1st Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_r(input_raw_with_centralized_level2, step=None, alpha=None, metric=jensenShannonDivergence)
        time_stop = time.time()
        print("2nd Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_r(input_raw_with_equalized_level2, step=None, alpha=None, metric=jensenShannonDivergence)
        time_stop = time.time()
        print("2nd Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

        print("[Test on Enhanced]")
        time_start = time.time()
        results = sdd_r(input_syn_with_centralized, step=level1_step_syn, alpha=None, metric=jensenShannonDivergence)
        time_stop = time.time()
        print("1st Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_r(input_syn_with_equalized, step=level1_step_syn, alpha=None, metric=jensenShannonDivergence)
        time_stop = time.time()
        print("1st Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_r(input_syn_with_centralized_level2, step=None, alpha=None, metric=jensenShannonDivergence)
        time_stop = time.time()
        print("2nd Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_r(input_syn_with_equalized_level2, step=None, alpha=None, metric=jensenShannonDivergence)
        time_stop = time.time()
        print("2nd Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        print()

        # 统计实验结果(SDD-R + α) #
        print(">>> SDD-R + α <<<")
        print("[Test on RAW]")
        time_start = time.time()
        results = sdd_r(input_raw_with_centralized, step=1, alpha=alpha, metric=jensenShannonDivergence)
        time_stop = time.time()
        print("1st Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_r(input_raw_with_equalized, step=1, alpha=alpha, metric=jensenShannonDivergence)
        time_stop = time.time()
        print("1st Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_r(input_raw_with_centralized_level2, step=None, alpha=alpha, metric=jensenShannonDivergence)
        time_stop = time.time()
        print("2nd Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_r(input_raw_with_equalized_level2, step=None, alpha=alpha, metric=jensenShannonDivergence)
        time_stop = time.time()
        print("2nd Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

        print("[Test on Enhanced]")
        time_start = time.time()
        results = sdd_r(input_syn_with_centralized, step=level1_step_syn, alpha=alpha, metric=jensenShannonDivergence)
        time_stop = time.time()
        print("1st Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_r(input_syn_with_equalized, step=level1_step_syn, alpha=alpha, metric=jensenShannonDivergence)
        time_stop = time.time()
        print("1st Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_r(input_syn_with_centralized_level2, step=None, alpha=alpha, metric=jensenShannonDivergence)
        time_stop = time.time()
        print("2nd Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_r(input_syn_with_equalized_level2, step=None, alpha=alpha, metric=jensenShannonDivergence)
        time_stop = time.time()
        print("2nd Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        print()

        # 统计实验结果(SDD-E Static) #
        print(">>> SDD-E Static <<<")
        print("[Test on RAW]")
        time_start = time.time()
        results = sdd_e(evidence_normal_raw, evidence_centralized_raw, input_raw_with_centralized, step=1,
                        alpha=None, metric=jensenShannonDivergence, dynamic=False)
        time_stop = time.time()
        print("1st Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_raw, evidence_equalized_raw, input_raw_with_equalized, step=1,
                        alpha=None, metric=jensenShannonDivergence, dynamic=False)
        time_stop = time.time()
        print("1st Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_raw_level2, evidence_centralized_raw_level2, input_raw_with_centralized_level2, step=None,
                        alpha=None, metric=jensenShannonDivergence, dynamic=False)
        time_stop = time.time()
        print("2nd Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_raw_level2, evidence_equalized_raw_level2, input_raw_with_equalized_level2, step=None,
                        alpha=None, metric=jensenShannonDivergence, dynamic=False)
        time_stop = time.time()
        print("2nd Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

        print("[Test on Enhanced]")
        time_start = time.time()
        results = sdd_e(evidence_normal_syn, evidence_centralized_syn, input_syn_with_centralized, step=level1_step_syn,
                        alpha=None, metric=jensenShannonDivergence, dynamic=False)
        time_stop = time.time()
        print("1st Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_syn, evidence_equalized_syn, input_syn_with_equalized, step=level1_step_syn,
                        alpha=None, metric=jensenShannonDivergence, dynamic=False)
        time_stop = time.time()
        print("1st Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_syn_level2, evidence_centralized_syn_level2, input_syn_with_centralized_level2, step=None,
                        alpha=None, metric=jensenShannonDivergence, dynamic=False)
        time_stop = time.time()
        print("2nd Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_syn_level2, evidence_equalized_syn_level2, input_syn_with_equalized_level2, step=None,
                        alpha=None, metric=jensenShannonDivergence, dynamic=False)
        time_stop = time.time()
        print("2nd Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        print()

        # 统计实验结果(SDD-E Static + α) #
        print(">>> SDD-E Static + α <<<")
        print("[Test on RAW]")
        time_start = time.time()
        results = sdd_e(evidence_normal_raw, evidence_centralized_raw, input_raw_with_centralized, step=1,
                        alpha=alpha, metric=jensenShannonDivergence, dynamic=False)
        time_stop = time.time()
        print("1st Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_raw, evidence_equalized_raw, input_raw_with_equalized, step=1,
                        alpha=alpha, metric=jensenShannonDivergence, dynamic=False)
        time_stop = time.time()
        print("1st Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_raw_level2, evidence_centralized_raw_level2, input_raw_with_centralized_level2, step=None,
                        alpha=alpha, metric=jensenShannonDivergence, dynamic=False)
        time_stop = time.time()
        print("2nd Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_raw_level2, evidence_equalized_raw_level2, input_raw_with_equalized_level2, step=None,
                        alpha=alpha, metric=jensenShannonDivergence, dynamic=False)
        time_stop = time.time()
        print("2nd Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

        print("[Test on Enhanced]")
        time_start = time.time()
        results = sdd_e(evidence_normal_syn, evidence_centralized_syn, input_syn_with_centralized, step=level1_step_syn,
                        alpha=alpha, metric=jensenShannonDivergence, dynamic=False)
        time_stop = time.time()
        print("1st Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_syn, evidence_equalized_syn, input_syn_with_equalized, step=level1_step_syn,
                        alpha=alpha, metric=jensenShannonDivergence, dynamic=False)
        time_stop = time.time()
        print("1st Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_syn_level2, evidence_centralized_syn_level2, input_syn_with_centralized_level2, step=None,
                        alpha=alpha, metric=jensenShannonDivergence, dynamic=False)
        time_stop = time.time()
        print("2nd Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_syn_level2, evidence_equalized_syn_level2, input_syn_with_equalized_level2, step=None,
                        alpha=alpha, metric=jensenShannonDivergence, dynamic=False)
        time_stop = time.time()
        print("2nd Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        print()

        # 统计实验结果(SDD-E Dynamic) #
        print(">>> SDD-E Dynamic <<<")
        print("[Test on RAW]")
        time_start = time.time()
        results = sdd_e(evidence_normal_raw, evidence_centralized_raw, input_raw_with_centralized, step=1,
                        alpha=None, metric=jensenShannonDivergence, dynamic=True)
        time_stop = time.time()
        print("1st Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_raw, evidence_equalized_raw, input_raw_with_equalized, step=1,
                        alpha=None, metric=jensenShannonDivergence, dynamic=True)
        time_stop = time.time()
        print("1st Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_raw_level2, evidence_centralized_raw_level2, input_raw_with_centralized_level2, step=None,
                        alpha=None, metric=jensenShannonDivergence, dynamic=True)
        time_stop = time.time()
        print("2nd Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_raw_level2, evidence_equalized_raw_level2, input_raw_with_equalized_level2, step=None,
                        alpha=None, metric=jensenShannonDivergence, dynamic=True)
        time_stop = time.time()
        print("2nd Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

        print("[Test on Enhanced]")
        time_start = time.time()
        results = sdd_e(evidence_normal_syn, evidence_centralized_syn, input_syn_with_centralized, step=level1_step_syn,
                        alpha=None, metric=jensenShannonDivergence, dynamic=True)
        time_stop = time.time()
        print("1st Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_syn, evidence_equalized_syn, input_syn_with_equalized, step=level1_step_syn,
                        alpha=None, metric=jensenShannonDivergence, dynamic=True)
        time_stop = time.time()
        print("1st Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_syn_level2, evidence_centralized_syn_level2, input_syn_with_centralized_level2, step=None,
                        alpha=None, metric=jensenShannonDivergence, dynamic=True)
        time_stop = time.time()
        print("2nd Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_syn_level2, evidence_equalized_syn_level2, input_syn_with_equalized_level2, step=None,
                        alpha=None, metric=jensenShannonDivergence, dynamic=True)
        time_stop = time.time()
        print("2nd Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        print()

        # 统计实验结果(SDD-E Dynamic + α) #
        print(">>> SDD-E Dynamic + α <<<")
        print("[Test on RAW]")
        time_start = time.time()
        results = sdd_e(evidence_normal_raw, evidence_centralized_raw, input_raw_with_centralized, step=1,
                        alpha=alpha, metric=jensenShannonDivergence, dynamic=True)
        time_stop = time.time()
        print("1st Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_raw, evidence_equalized_raw, input_raw_with_equalized, step=1,
                        alpha=alpha, metric=jensenShannonDivergence, dynamic=True)
        time_stop = time.time()
        print("1st Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_raw_level2, evidence_centralized_raw_level2, input_raw_with_centralized_level2, step=None,
                        alpha=alpha, metric=jensenShannonDivergence, dynamic=True)
        time_stop = time.time()
        print("2nd Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_raw_level2, evidence_equalized_raw_level2, input_raw_with_equalized_level2, step=None,
                        alpha=alpha, metric=jensenShannonDivergence, dynamic=True)
        time_stop = time.time()
        print("2nd Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

        print("[Test on Enhanced]")
        time_start = time.time()
        results = sdd_e(evidence_normal_syn, evidence_centralized_syn, input_syn_with_centralized, step=level1_step_syn,
                        alpha=alpha, metric=jensenShannonDivergence, dynamic=True)
        time_stop = time.time()
        print("1st Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_syn, evidence_equalized_syn, input_syn_with_equalized, step=level1_step_syn,
                        alpha=alpha, metric=jensenShannonDivergence, dynamic=True)
        time_stop = time.time()
        print("1st Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_syn_level2, evidence_centralized_syn_level2, input_syn_with_centralized_level2, step=None,
                        alpha=alpha, metric=jensenShannonDivergence, dynamic=True)
        time_stop = time.time()
        print("2nd Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = sdd_e(evidence_normal_syn_level2, evidence_equalized_syn_level2, input_syn_with_equalized_level2, step=None,
                        alpha=alpha, metric=jensenShannonDivergence, dynamic=True)
        time_stop = time.time()
        print("2nd Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        print()

        # 统计实验结果(MGoF) #
        print(">>> MGoF <<<")
        print("[Test on RAW]")
        time_start = time.time()
        results = mgof(input_raw_with_centralized)
        time_stop = time.time()
        print("1st Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = mgof(input_raw_with_equalized)
        time_stop = time.time()
        print("1st Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = mgof(input_raw_with_centralized_level2)
        time_stop = time.time()
        print("2nd Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = mgof(input_raw_with_equalized_level2)
        time_stop = time.time()
        print("2nd Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

        print("[Test on Enhanced]")
        time_start = time.time()
        results = mgof(input_syn_with_centralized)
        time_stop = time.time()
        print("1st Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = mgof(input_syn_with_equalized)
        time_stop = time.time()
        print("1st Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = mgof(input_syn_with_centralized_level2)
        time_stop = time.time()
        print("2nd Level Centralized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        time_start = time.time()
        results = mgof(input_syn_with_equalized_level2)
        time_stop = time.time()
        print("2nd Level Equalized: ")
        TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data_raw), anomaly_indices, results)
        print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))
        print()

        print()
        print("----------------------------------------")
        print()
    print("Done.")


def testDifferentAnomalyProbability():
    print("Testing Different Anomaly Probabilities...")
    # 加载数据集 #
    correct_data = loadCollectionFromFile("Koubei/SynCorrect.csv")
    centralized_data = loadCollectionFromFile("Koubei/SynCentralized.csv")
    equalized_data = loadCollectionFromFile("Koubei/SynEqualized.csv")

    for i in range(1, 10):
        print("----------------------------------------")
        alpha = i / 10
        print(">> ALPHA=%f" % alpha)
        num_anomalies = int(alpha * len(correct_data))
        # 随机生成异常序列 #
        anomaly_indices_array = [
            sorted(np.random.choice(range(len(correct_data)), num_anomalies, replace=False)) for i in range(EXP_DUPLICATE)
        ]

        # 计算1st level直方图的步长 #
        sample = correct_data[0]
        sample_sigma = statistics.stdev(sample)
        level1_step = 1.05 * sample_sigma * (len(sample) ** -0.2)

        # 分组进行实验 #
        for anomaly_indices in anomaly_indices_array:
            print("Anomalies(#=%d): " % len(anomaly_indices), anomaly_indices)
            # 构造输入数据 #
            evidence_normal_1st_level = correct_data[:30]
            evidence_centralized = centralized_data[:10]
            evidence_normal_2nd_level = [histogram(collection, level1_step)[0].values() for collection in evidence_normal_1st_level]
            evidence_equalized = [histogram(collection, level1_step)[0].values() for collection in equalized_data[:10]]

            input_with_centralized = correct_data.copy()
            level1_with_equalized = correct_data.copy()
            for idx in anomaly_indices:
                input_with_centralized[idx] = centralized_data[idx]
                level1_with_equalized[idx] = equalized_data[idx]
            input_with_equalized = [histogram(collection, level1_step)[0].values() for collection in level1_with_equalized]

            # 统计实验结果(SDD-R) #
            time_centralized_start = time.time()
            centralized_detect_results = sdd_r(input_with_centralized, step=level1_step, alpha=None, metric=jensenShannonDivergence)
            time_centralized_stop = time.time()
            equalized_detect_results = sdd_r(input_with_equalized, alpha=None, metric=jensenShannonDivergence)
            time_equalized_stop = time.time()

            print("Centralized Results(SDD-R): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, centralized_detect_results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_centralized_stop - time_centralized_start) * 1000))
            print("Equalized Results(SDD-R): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, equalized_detect_results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_equalized_stop - time_centralized_stop) * 1000))
            print()

            # 统计实验结果(SDD-R+) #
            time_centralized_start = time.time()
            centralized_detect_results = sdd_r(input_with_centralized, step=level1_step, alpha=alpha, metric=jensenShannonDivergence)
            time_centralized_stop = time.time()
            equalized_detect_results = sdd_r(input_with_equalized, alpha=alpha, metric=jensenShannonDivergence)
            time_equalized_stop = time.time()

            print("Centralized Results(SDD-R+): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, centralized_detect_results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_centralized_stop - time_centralized_start) * 1000))
            print("Equalized Results(SDD-R+): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, equalized_detect_results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_equalized_stop - time_centralized_stop) * 1000))
            print()

            # 统计实验结果(SDD-E Static) #
            time_centralized_start = time.time()
            centralized_detect_results = sdd_e(
                evidence_normal_1st_level, evidence_centralized, input_with_centralized,
                step=level1_step, alpha=None, metric=jensenShannonDivergence, dynamic=False
            )
            time_centralized_stop = time.time()
            equalized_detect_results = sdd_e(
                evidence_normal_2nd_level, evidence_equalized, input_with_equalized,
                alpha=None, metric=jensenShannonDivergence, dynamic=False
            )
            time_equalized_stop = time.time()

            print("Centralized Results(SDD-E Static): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, centralized_detect_results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_centralized_stop - time_centralized_start) * 1000))
            print("Equalized Results(SDD-E Static): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, equalized_detect_results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_equalized_stop - time_centralized_stop) * 1000))
            print()

            # 统计实验结果(SDD-E Static+) #
            time_centralized_start = time.time()
            centralized_detect_results = sdd_e(
                evidence_normal_1st_level, evidence_centralized, input_with_centralized,
                step=level1_step, alpha=alpha, metric=jensenShannonDivergence, dynamic=False
            )
            time_centralized_stop = time.time()
            equalized_detect_results = sdd_e(
                evidence_normal_2nd_level, evidence_equalized, input_with_equalized,
                alpha=alpha, metric=jensenShannonDivergence, dynamic=False
            )
            time_equalized_stop = time.time()

            print("Centralized Results(SDD-E Static+): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, centralized_detect_results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_centralized_stop - time_centralized_start) * 1000))
            print("Equalized Results(SDD-E Static+): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, equalized_detect_results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_equalized_stop - time_centralized_stop) * 1000))
            print()

            # 统计实验结果(SDD-E Dynamic) #
            time_centralized_start = time.time()
            centralized_detect_results = sdd_e(
                evidence_normal_1st_level, evidence_centralized, input_with_centralized,
                step=level1_step, alpha=None, metric=jensenShannonDivergence, dynamic=True
            )
            time_centralized_stop = time.time()
            equalized_detect_results = sdd_e(
                evidence_normal_2nd_level, evidence_equalized, input_with_equalized,
                alpha=None, metric=jensenShannonDivergence, dynamic=True
            )
            time_equalized_stop = time.time()

            print("Centralized Results(SDD-E Dynamic): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, centralized_detect_results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_centralized_stop - time_centralized_start) * 1000))
            print("Equalized Results(SDD-E Dynamic): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, equalized_detect_results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_equalized_stop - time_centralized_stop) * 1000))
            print()

            # 统计实验结果(SDD-E Dynamic+) #
            time_centralized_start = time.time()
            centralized_detect_results = sdd_e(
                evidence_normal_1st_level, evidence_centralized, input_with_centralized,
                step=level1_step, alpha=alpha, metric=jensenShannonDivergence, dynamic=True
            )
            time_centralized_stop = time.time()
            equalized_detect_results = sdd_e(
                evidence_normal_2nd_level, evidence_equalized, input_with_equalized,
                alpha=alpha, metric=jensenShannonDivergence, dynamic=True
            )
            time_equalized_stop = time.time()

            print("Centralized Results(SDD-E Dynamic+): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, centralized_detect_results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_centralized_stop - time_centralized_start) * 1000))
            print("Equalized Results(SDD-E Dynamic+): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, equalized_detect_results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_equalized_stop - time_centralized_stop) * 1000))
            print()

            # 统计实验结果(SDD-E MGoF) #
            time_centralized_start = time.time()
            centralized_detect_results = mgof(input_with_centralized)
            time_centralized_stop = time.time()
            equalized_detect_results = mgof(input_with_equalized)
            time_equalized_stop = time.time()

            print("Centralized Results(MGoF): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, centralized_detect_results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_centralized_stop - time_centralized_start) * 1000))
            print("Equalized Results(MGoF): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, equalized_detect_results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_equalized_stop - time_centralized_stop) * 1000))

            print()
        print("----------------------------------------")
    print("Done")


def testDifferentAnomalyMagintude():
    print("Testing Different Anomaly Magnitudes...")
    # 加载数据集 #
    correct_data = loadCollectionFromFile("Koubei/SynCorrect.csv")

    # 计算1st level直方图的步长 #
    sample = correct_data[0]
    sample_sigma = statistics.stdev(sample)
    step = 1.05 * sample_sigma * (len(sample) ** -0.2)

    # 设置参数 #
    alpha = 0.1
    num_anomalies = int(alpha * len(correct_data))
    evidence_normal = correct_data[:30]

    # 随机生成异常序列 #
    anomaly_indices_array = [
        sorted(np.random.choice(range(len(correct_data)), num_anomalies, replace=False)) for i in range(EXP_DUPLICATE)
    ]
    print("Anomalies:")
    for i in range(EXP_DUPLICATE):
        print(anomaly_indices_array[i])

    # 对不同的异常程度进行实验 #
    for magnitude in range(1, 10):
        print("----------------------------------------")
        print("Magnitude: x1.%d" % magnitude)
        centralized_data = loadCollectionFromFile("Koubei/SynCentralized(1.%d).csv" % magnitude)
        evidence_anomalous = centralized_data[:10]

        # 进行重复实验 #
        for i in range(EXP_DUPLICATE):
            print(">>> [DUP #%d]" % i)
            anomaly_indices = anomaly_indices_array[i]

            # 构造输入数据 #
            input_with_centralized = correct_data.copy()
            for idx in anomaly_indices:
                input_with_centralized[idx] = centralized_data[idx]

            # 统计实验结果(SDD-R) #
            time_start = time.time()
            results = sdd_r(input_with_centralized, step=step, alpha=None, metric=jensenShannonDivergence)
            time_stop = time.time()
            print("Results(SDD-R): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            # 统计实验结果(SDD-R+) #
            time_start = time.time()
            results = sdd_r(input_with_centralized, step=step, alpha=alpha, metric=jensenShannonDivergence)
            time_stop = time.time()
            print("Results(SDD-R+): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            # 统计实验结果(SDD-E Static) #
            time_start = time.time()
            results = sdd_e(
                evidence_normal, evidence_anomalous, input_with_centralized, step=step, alpha=None,
                metric=jensenShannonDivergence, dynamic=False
            )
            time_stop = time.time()
            print("Results(SDD-E Static): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            # 统计实验结果(SDD-E Static+) #
            time_start = time.time()
            results = sdd_e(
                evidence_normal, evidence_anomalous, input_with_centralized, step=step, alpha=alpha,
                metric=jensenShannonDivergence, dynamic=False
            )
            time_stop = time.time()
            print("Results(SDD-E Static+): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            # 统计实验结果(SDD-E Dynamic) #
            time_start = time.time()
            results = sdd_e(
                evidence_normal, evidence_anomalous, input_with_centralized, step=step, alpha=None,
                metric=jensenShannonDivergence, dynamic=True
            )
            time_stop = time.time()
            print("Results(SDD-E Dynamic): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            # 统计实验结果(SDD-E Dynamic+) #
            time_start = time.time()
            results = sdd_e(
                evidence_normal, evidence_anomalous, input_with_centralized, step=step, alpha=alpha,
                metric=jensenShannonDivergence, dynamic=True
            )
            time_stop = time.time()
            print("Results(SDD-E Dynamic+): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            # 统计实验结果(MGoF) #
            time_start = time.time()
            results = mgof(input_with_centralized)
            time_stop = time.time()
            print("Results(MGoF): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            print()
        print("----------------------------------------")
    print("Done.")


def testPerformanceOnSyntheticData():
    print("Testing Performance on Synthetic Data...")
    # 设置参数 #
    alpha = 0.1
    data_file_prefixes = [
        "Uniform",
        "Gaussian",
        "RandShape",
        "RandShapeWithDrift"
    ]

    # 按数据分类进行实验 #
    for prefix in data_file_prefixes:
        print("-------------------[%s]---------------------" % prefix)
        # 加载数据 #
        correct_data = loadCollectionFromFile("Synthetic/%sCorrect.csv" % prefix)
        anomalous_data = loadCollectionFromFile("Synthetic/%sAnomalous.csv" % prefix)

        # 随机生成异常序列 #
        num_anomalies = int(alpha * len(correct_data))
        anomaly_indices_array = [
            sorted(np.random.choice(range(len(correct_data)), num_anomalies, replace=False)) for i in range(EXP_DUPLICATE)
        ]
        print("Anomalies:")
        for i in range(EXP_DUPLICATE):
            print(anomaly_indices_array[i])

        # 设置参数 #
        evidence_normal = correct_data[:len(correct_data) // 10]
        evidence_anomalous = anomalous_data[:int(len(anomalous_data) * alpha / 3)]

        # 计算直方图的步长 #
        sample = correct_data[0]
        sample_sigma = statistics.stdev(sample)
        step = 1.05 * sample_sigma * (len(sample) ** -0.2)

        # 重复试验 #
        for i in range(EXP_DUPLICATE):
            print(">>> [DUP #%d]" % i)
            anomaly_indices = anomaly_indices_array[i]

            # 构造输入数据 #
            input_data = correct_data.copy()
            for idx in anomaly_indices:
                input_data[idx] = anomalous_data[idx]

            # 统计实验结果(SDD-R) #
            time_start = time.time()
            results = sdd_r(input_data, step=step, alpha=None, metric=jensenShannonDivergence)
            time_stop = time.time()
            print("Results(SDD-R): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            # 统计实验结果(SDD-R+) #
            time_start = time.time()
            results = sdd_r(input_data, step=step, alpha=alpha, metric=jensenShannonDivergence)
            time_stop = time.time()
            print("Results(SDD-R+): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            # 统计实验结果(SDD-E Static) #
            time_start = time.time()
            results = sdd_e(
                evidence_normal, evidence_anomalous, input_data, step=step, alpha=None,
                metric=jensenShannonDivergence, dynamic=False
            )
            time_stop = time.time()
            print("Results(SDD-E Static): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            # 统计实验结果(SDD-E Static+) #
            time_start = time.time()
            results = sdd_e(
                evidence_normal, evidence_anomalous, input_data, step=step, alpha=alpha,
                metric=jensenShannonDivergence, dynamic=False
            )
            time_stop = time.time()
            print("Results(SDD-E Static+): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            # 统计实验结果(SDD-E Dynamic) #
            time_start = time.time()
            results = sdd_e(
                evidence_normal, evidence_anomalous, input_data, step=step, alpha=None,
                metric=jensenShannonDivergence, dynamic=True
            )
            time_stop = time.time()
            print("Results(SDD-E Dynamic): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            # 统计实验结果(SDD-E Dynamic+) #
            time_start = time.time()
            results = sdd_e(
                evidence_normal, evidence_anomalous, input_data, step=step, alpha=alpha,
                metric=jensenShannonDivergence, dynamic=True
            )
            time_stop = time.time()
            print("Results(SDD-E Dynamic+): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            # 统计实验结果(MGoF) #
            time_start = time.time()
            results = mgof(input_data)
            time_stop = time.time()
            print("Results(MGoF): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            print()
        print("----------------------------------------")
        print()
    print("Done.")


def testDifferentDivergenceMetric():
    print("Testing Different Divergence Metric...")
    # 加载数据集 #
    correct_data = loadCollectionFromFile("Synthetic/RandShapeCorrect.csv")
    anomalous_data = loadCollectionFromFile("Synthetic/RandShapeAnomalous.csv")

    # 设置参数 #
    sample = correct_data[0]
    sample_sigma = statistics.stdev(sample)
    step = 1.05 * sample_sigma * (len(sample) ** -0.2)
    alpha = 0.1
    num_anomalies = int(alpha * len(correct_data))
    anomaly_indices_array = [
        sorted(np.random.choice(range(len(correct_data)), num_anomalies, replace=False)) for i in range(EXP_DUPLICATE)
    ]
    print("Anomalies:")
    for i in range(EXP_DUPLICATE):
        print(anomaly_indices_array[i])
    evidence_normal = correct_data[:len(correct_data) // 10]
    evidence_anomalous = anomalous_data[:int(len(anomalous_data) * alpha / 3)]

    # 分类进行实验 #
    metrics = [
        kullbackLeiblerDivergence,
        jensenShannonDivergence,
        bhattacharyyaDistance,
        hellingerDistance,
        kolmogorovSmirnovStatistic
    ]
    for metric in metrics:
        print("-------------------[%s]---------------------" % metric.__name__)
        # 重复试验 #
        for anomaly_indices in anomaly_indices_array:
            # 构造输入数据 #
            input_data = correct_data.copy()
            for idx in anomaly_indices:
                input_data[idx] = anomalous_data[idx]

            # 统计实验结果(SDD-R) #
            time_start = time.time()
            results = sdd_r(input_data, step=step, alpha=None, metric=metric)
            time_stop = time.time()
            print("Results(SDD-R): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            # 统计实验结果(SDD-R+) #
            time_start = time.time()
            results = sdd_r(input_data, step=step, alpha=alpha, metric=metric)
            time_stop = time.time()
            print("Results(SDD-R+): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            # 统计实验结果(SDD-E Static) #
            time_start = time.time()
            results = sdd_e(evidence_normal, evidence_anomalous, input_data, step=step, alpha=None, metric=metric, dynamic=False)
            time_stop = time.time()
            print("Results(SDD-E Static): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            # 统计实验结果(SDD-E Static+) #
            time_start = time.time()
            results = sdd_e(evidence_normal, evidence_anomalous, input_data, step=step, alpha=alpha, metric=metric, dynamic=False)
            time_stop = time.time()
            print("Results(SDD-E Static+): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            # 统计实验结果(SDD-E Dynamic) #
            time_start = time.time()
            results = sdd_e(evidence_normal, evidence_anomalous, input_data, step=step, alpha=None, metric=metric, dynamic=True)
            time_stop = time.time()
            print("Results(SDD-E Dynamic): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            # 统计实验结果(SDD-E Dynamic+) #
            time_start = time.time()
            results = sdd_e(evidence_normal, evidence_anomalous, input_data, step=step, alpha=alpha, metric=metric, dynamic=True)
            time_stop = time.time()
            print("Results(SDD-E Dynamic+): ")
            TP, TN, FP, FN = calculateConfusionMatrix(len(correct_data), anomaly_indices, results)
            print("%d\t%d\t%d\t%d\t%f" % (TP, TN, FP, FN, (time_stop - time_start) * 1000))

            print()
        print("----------------------------------------")
        print()
    print("Done.")


def testROC():
    print("Testing ROC of Different Divergence Metric...")
    # 加载数据集 #
    correct_data = loadCollectionFromFile("Synthetic/RandShapeCorrect.csv")
    anomalous_data = loadCollectionFromFile("Synthetic/RandShapeAnomalous.csv")

    # 设置参数 #
    sample = correct_data[0]
    sample_sigma = statistics.stdev(sample)
    step = 1.05 * sample_sigma * (len(sample) ** -0.2)
    alpha = 0.1
    num_anomalies = int(alpha * len(correct_data))
    anomaly_indices_array = [
        sorted(np.random.choice(range(len(correct_data)), num_anomalies, replace=False)) for i in range(EXP_DUPLICATE)
    ]
    print("Anomalies:")
    for i in range(EXP_DUPLICATE):
        print(anomaly_indices_array[i])
    evidence_normal = correct_data[:len(correct_data) // 10]

    # 分类进行实验 #
    metric_shortname = {
        kullbackLeiblerDivergence: "KLD",
        jensenShannonDivergence: "JSD",
        bhattacharyyaDistance: "BD",
        hellingerDistance: "HD",
        kolmogorovSmirnovStatistic: "KSS"
    }
    for metric, shortname in metric_shortname.items():
        print("-------------------[%s]---------------------" % shortname)
        # 重复试验 #
        sdd_e_orders = []
        sdd_r_orders = []
        for anomaly_indices in anomaly_indices_array:
            # 构造输入数据 #
            input_data = correct_data.copy()
            for idx in anomaly_indices:
                input_data[idx] = anomalous_data[idx]

            # 进行异常度排序 #
            print("Ordering...")
            sdd_e_orders.append(sdd_e_rank(evidence_normal, input_data, step=step, metric=metric))
            sdd_r_orders.append(sdd_r_rank(input_data, step=step, metric=metric))

        # 统计结果 #
        print("Results(SDD-E): ")
        output_file = open("Exp-ROC(SDD-E)-%s.csv" % shortname, 'w')
        result = calculateROC(anomaly_indices_array, sdd_e_orders)
        output_file.writelines("%f\t%f\n" % (FPR, TPR) for FPR, TPR in result)
        output_file.close()

        print("Results(SDD-R): ")
        output_file = open("Exp-ROC(SDD-R)-%s.csv" % shortname, 'w')
        result = calculateROC(anomaly_indices_array, sdd_r_orders)
        output_file.writelines("%f\t%f\n" % (FPR, TPR) for FPR, TPR in result)
        output_file.close()

        print("----------------------------------------")
        print()
    print("Done.")


if __name__ == '__main__':
    print("Running Experiments...")
    # testPerformanceOnKoubei()
    # testDifferentAnomalyProbability()
    # testDifferentAnomalyMagintude()
    # testPerformanceOnSyntheticData()
    # testDifferentDivergenceMetric()
    testROC()
    print("All Done.")
