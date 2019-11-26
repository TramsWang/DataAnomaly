def loadCollectionFromFile(path):
    """
    根据数据文件的固定格式加载数据。

    :param path: 数据文件路径
    :return: 数据群的列表
    """
    data_file = open(path, 'r')
    data = data_file.readlines()
    collection = [[float(num) for num in line.strip('\n').split('\t')] for line in data]
    data_file.close()
    return collection


def calculateConfusionMatrix(sample_size, anomalies, predicted_anomalies):
    TP = 0
    FP = 0
    for i in predicted_anomalies:
        if i in anomalies:
            TP += 1
        else:
            FP += 1
    FN = len(anomalies) - TP
    TN = sample_size - len(anomalies) - FP
    return TP, TN, FP, FN


def calculateROC(anomaly_array, ranked_array):
    # 计算所有的混淆矩阵 #
    confusion_matrix_lists = []
    for i in range(len(anomaly_array)):
        anomaly = anomaly_array[i]
        rank = ranked_array[i]
        confusion_matrix_list = []
        for k in range(len(rank)):
            confusion_matrix_list.append(calculateConfusionMatrix(len(rank), anomaly, rank[:k]))
        confusion_matrix_lists.append(confusion_matrix_list)

    # 对所有对应位置的混淆矩阵求平均 #
    average_confusion_matrix_list = []
    for k in range(len(confusion_matrix_lists[0])):
        confusion_matrixes = [confusion_matrix_list[k] for confusion_matrix_list in confusion_matrix_lists]
        dim_len = len(confusion_matrixes[0])
        average_confusion_matrix = tuple(
            sum(confusion_matrix[dim] for confusion_matrix in confusion_matrixes) / len(confusion_matrixes)
            for dim in range(dim_len)
        )
        average_confusion_matrix_list.append(average_confusion_matrix)
        # for t in average_confusion_matrix_list:
        #     s = ''
        #     for v in t:
        #         s += str(v) + ','
        #     print(s)
        # print("-----")

    # 根据绘制点的数量要求找到绘制点，使点在图像上尽量平均 #
    coordinates = [(FP / (FP + TN), TP / (TP + FN)) for TP, TN, FP, FN in average_confusion_matrix_list]
    # first_half = round(points / 2)
    # last_half = points - 1 - first_half
    return coordinates


if __name__ == '__main__':
    calculateROC(
        [
            [1,2,3],
            [1,2,3]
        ],
        [
            [1,4,2,5,3],
            [1,2,4,5,3]
        ]
    )