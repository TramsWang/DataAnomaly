import numpy as np
from Utils import *


def genUniform(collection_size, sample_size):
    COLLECTION_SIZE = collection_size
    SAMPLE_SIZE = sample_size
    print()

    # Generate Correct Data Collections #
    INFIMUM = 0
    SUPREMUM = 10
    FLUCTUATION = 5

    print("Generating Correct Uniform Samples...")
    output_file = open("Synthetic/UniformCorrect.csv", 'w')
    for _ in range(SAMPLE_SIZE):
        infimum = INFIMUM + FLUCTUATION * np.random.random() - FLUCTUATION / 2
        supremum = SUPREMUM + FLUCTUATION * np.random.random() - FLUCTUATION / 2
        collection = (supremum - infimum) * np.random.random_sample(COLLECTION_SIZE) + infimum
        output_file.write("%f" % collection[0])
        output_file.writelines("\t%f" % collection[i] for i in range(1, COLLECTION_SIZE))
        output_file.write('\n')
    output_file.close()

    print("Generating Anomalous Uniform Samples...")
    # Generate Anomalous Data Collections #
    INFIMUM -= FLUCTUATION
    SUPREMUM += FLUCTUATION

    output_file = open("Synthetic/UniformAnomalous.csv", 'w')
    for _ in range(SAMPLE_SIZE):
        infimum = INFIMUM + FLUCTUATION * np.random.random() - FLUCTUATION / 2
        supremum = SUPREMUM + FLUCTUATION * np.random.random() - FLUCTUATION / 2
        collection = (supremum - infimum) * np.random.random_sample(COLLECTION_SIZE) + infimum
        output_file.write("%f" % collection[0])
        output_file.writelines("\t%f" % collection[i] for i in range(1, COLLECTION_SIZE))
        output_file.write('\n')
    output_file.close()

    print("Uniform Distribution Generation Done.")


def genGaussian(collection_size, sample_size):
    COLLECTION_SIZE = collection_size
    SAMPLE_SIZE = sample_size
    print()

    # Generate Correct Data Collections #
    MU = 0
    SIGMA = 1
    MU_FLUCTUATION = 1
    SIGMA_FLUCTUATION = 1

    print("Generating Correct Gaussian Samples...")
    output_file = open("Synthetic/GaussianCorrect.csv", 'w')
    for _ in range(SAMPLE_SIZE):
        mu = MU + MU_FLUCTUATION * np.random.random() - MU_FLUCTUATION / 2
        sigma = SIGMA + SIGMA_FLUCTUATION * np.random.random() - SIGMA_FLUCTUATION / 2
        collection = np.random.normal(mu, sigma, COLLECTION_SIZE)
        output_file.write("%f" % collection[0])
        output_file.writelines("\t%f" % collection[i] for i in range(1, COLLECTION_SIZE))
        output_file.write('\n')
    output_file.close()

    # Generate Anomalous Data Collections #
    MU_FLUCTUATION *= 2
    SIGMA *= 2
    SIGMA_FLUCTUATION *= 2

    print("Generating Anomalous Gaussian Samples...")
    output_file = open("Synthetic/GaussianAnomalous.csv", 'w')
    for _ in range(SAMPLE_SIZE):
        mu = MU + MU_FLUCTUATION * np.random.random() - MU_FLUCTUATION / 2
        sigma = SIGMA + SIGMA_FLUCTUATION * np.random.random() - SIGMA_FLUCTUATION / 2
        collection = np.random.normal(mu, sigma, COLLECTION_SIZE)
        output_file.write("%f" % collection[0])
        output_file.writelines("\t%f" % collection[i] for i in range(1, COLLECTION_SIZE))
        output_file.write('\n')
    output_file.close()

    print("Gaussian Distribution Generation Done.")


def genRandomShape(collection_size, sample_size):
    COLLECTION_SIZE = collection_size
    SAMPLE_SIZE = sample_size
    # Generate Correct Data Collections #
    INFIMUM = 0
    SUPREMUM = 10
    UNIFORM_FLUCTUATION = 5
    MU1 = 5
    SIGMA1 = 0.5
    GAUSSIAN_PROPORTION1 = int(COLLECTION_SIZE * 0.2)
    MU1_FLUCTUATION = 1
    SIGMA1_FLUCTUATION = 0.5
    MU2 = 8
    SIGMA2 = 2
    GAUSSIAN_PROPORTION2 = int(COLLECTION_SIZE * 0.3)
    MU2_FLUCTUATION = 2
    SIGMA2_FLUCTUATION = 2

    print()
    print("Generating Correct Random-shape Distribution Samples...")
    output_file = open("Synthetic/RandShapeCorrect.csv", 'w')
    for _ in range(SAMPLE_SIZE):
        infimum = INFIMUM + UNIFORM_FLUCTUATION * np.random.random() - UNIFORM_FLUCTUATION / 2
        supremum = SUPREMUM + UNIFORM_FLUCTUATION * np.random.random() - UNIFORM_FLUCTUATION / 2
        mu1 = MU1 + MU1_FLUCTUATION * np.random.random() - MU1_FLUCTUATION / 2
        sigma1 = SIGMA1 + SIGMA1_FLUCTUATION * np.random.random() - SIGMA1_FLUCTUATION / 2
        mu2 = MU2 + MU2_FLUCTUATION * np.random.random() - MU2_FLUCTUATION / 2
        sigma2 = SIGMA2 + SIGMA2_FLUCTUATION * np.random.random() - SIGMA2_FLUCTUATION / 2
        uniform_collection = (supremum - infimum) * np.random.random_sample(
            COLLECTION_SIZE - GAUSSIAN_PROPORTION1 - GAUSSIAN_PROPORTION2
        ) + infimum
        gaussian_collection1 = np.random.normal(mu1, sigma1, GAUSSIAN_PROPORTION1)
        gaussian_collection2 = np.random.normal(mu2, sigma2, GAUSSIAN_PROPORTION2)
        output_file.write("%f" % uniform_collection[0])
        output_file.writelines("\t%f" % uniform_collection[i] for i in range(1, len(uniform_collection)))
        output_file.writelines("\t%f" % gaussian_collection1[i] for i in range(len(gaussian_collection1)))
        output_file.writelines("\t%f" % gaussian_collection2[i] for i in range(len(gaussian_collection2)))
        output_file.write('\n')
    output_file.close()

    # Generate Anomalous Data Collections #
    INFIMUM -= UNIFORM_FLUCTUATION
    SUPREMUM += UNIFORM_FLUCTUATION
    MU1_FLUCTUATION *= 2
    SIGMA1 *= 2
    SIGMA1_FLUCTUATION *= 2
    MU2_FLUCTUATION *= 2
    SIGMA2 *= 2
    SIGMA2_FLUCTUATION *= 2

    print("Generating Anomalous Random-shape Distribution Samples...")
    output_file = open("Synthetic/RandShapeAnomalous.csv", 'w')
    for _ in range(SAMPLE_SIZE):
        infimum = INFIMUM + UNIFORM_FLUCTUATION * np.random.random() - UNIFORM_FLUCTUATION / 2
        supremum = SUPREMUM + UNIFORM_FLUCTUATION * np.random.random() - UNIFORM_FLUCTUATION / 2
        mu1 = MU1 + MU1_FLUCTUATION * np.random.random() - MU1_FLUCTUATION / 2
        sigma1 = SIGMA1 + SIGMA1_FLUCTUATION * np.random.random() - SIGMA1_FLUCTUATION / 2
        mu2 = MU2 + MU2_FLUCTUATION * np.random.random() - MU2_FLUCTUATION / 2
        sigma2 = SIGMA2 + SIGMA2_FLUCTUATION * np.random.random() - SIGMA2_FLUCTUATION / 2
        uniform_collection = (supremum - infimum) * np.random.random_sample(
            COLLECTION_SIZE - GAUSSIAN_PROPORTION1 - GAUSSIAN_PROPORTION2
        ) + infimum
        gaussian_collection1 = np.random.normal(mu1, sigma1, GAUSSIAN_PROPORTION1)
        gaussian_collection2 = np.random.normal(mu2, sigma2, GAUSSIAN_PROPORTION2)
        output_file.write("%f" % uniform_collection[0])
        output_file.writelines("\t%f" % uniform_collection[i] for i in range(1, len(uniform_collection)))
        output_file.writelines("\t%f" % gaussian_collection1[i] for i in range(len(gaussian_collection1)))
        output_file.writelines("\t%f" % gaussian_collection2[i] for i in range(len(gaussian_collection2)))
        output_file.write('\n')
    output_file.close()

    print("Random-shape Distribution Generation Done.")


def genRandomShapeDrifted(collection_size, sample_size, drift_step):
    # COLLECTION_SIZE = collection_size
    # SAMPLE_SIZE = sample_size
    # DRIFT_STEP = drift_step
    # # Generate Correct Data Collections #
    # INFIMUM = 0
    # SUPREMUM = 10
    # UNIFORM_FLUCTUATION = 5
    # MU1 = 5
    # SIGMA1 = 0.5
    # GAUSSIAN_PROPORTION1 = int(COLLECTION_SIZE * 0.2)
    # MU1_FLUCTUATION = 1
    # SIGMA1_FLUCTUATION = 0.5
    # MU2 = 8
    # SIGMA2 = 2
    # GAUSSIAN_PROPORTION2 = int(COLLECTION_SIZE * 0.3)
    # MU2_FLUCTUATION = 2
    # SIGMA2_FLUCTUATION = 2
    #
    # print()
    # print("Generating Correct Random-shape Distribution(with Drift) Samples...")
    # output_file = open("Synthetic/RandShapeWithDriftCorrect.csv", 'w')
    # for drift in [dft * DRIFT_STEP for dft in range(SAMPLE_SIZE)]:
    #     infimum = INFIMUM + UNIFORM_FLUCTUATION * np.random.random() - UNIFORM_FLUCTUATION / 2
    #     supremum = SUPREMUM + UNIFORM_FLUCTUATION * np.random.random() - UNIFORM_FLUCTUATION / 2
    #     mu1 = MU1 + MU1_FLUCTUATION * np.random.random() - MU1_FLUCTUATION / 2
    #     sigma1 = SIGMA1 + SIGMA1_FLUCTUATION * np.random.random() - SIGMA1_FLUCTUATION / 2
    #     mu2 = MU2 + MU2_FLUCTUATION * np.random.random() - MU2_FLUCTUATION / 2
    #     sigma2 = SIGMA2 + SIGMA2_FLUCTUATION * np.random.random() - SIGMA2_FLUCTUATION / 2
    #     uniform_collection = (supremum - infimum) * np.random.random_sample(
    #         COLLECTION_SIZE - GAUSSIAN_PROPORTION1 - GAUSSIAN_PROPORTION2
    #     ) + infimum
    #     gaussian_collection1 = np.random.normal(mu1, sigma1, GAUSSIAN_PROPORTION1)
    #     gaussian_collection2 = np.random.normal(mu2, sigma2, GAUSSIAN_PROPORTION2)
    #     collection = drift + np.concatenate((uniform_collection, gaussian_collection1, gaussian_collection2))
    #     output_file.write("%f" % collection[0])
    #     output_file.writelines("\t%f" % collection[i] for i in range(1, COLLECTION_SIZE))
    #     output_file.write('\n')
    # output_file.close()
    #
    # # Generate Anomalous Data Collections #
    # INFIMUM -= UNIFORM_FLUCTUATION
    # SUPREMUM += UNIFORM_FLUCTUATION
    # MU1_FLUCTUATION *= 2
    # SIGMA1 *= 2
    # SIGMA1_FLUCTUATION *= 2
    # MU2_FLUCTUATION *= 2
    # SIGMA2 *= 2
    # SIGMA2_FLUCTUATION *= 2
    #
    # print("Generating Anomalous Random-shape Distribution(with Drift) Samples...")
    # output_file = open("Synthetic/RandShapeWithDriftAnomalous.csv", 'w')
    # for drift in [dft * DRIFT_STEP for dft in range(SAMPLE_SIZE)]:
    #     infimum = INFIMUM + UNIFORM_FLUCTUATION * np.random.random() - UNIFORM_FLUCTUATION / 2
    #     supremum = SUPREMUM + UNIFORM_FLUCTUATION * np.random.random() - UNIFORM_FLUCTUATION / 2
    #     mu1 = MU1 + MU1_FLUCTUATION * np.random.random() - MU1_FLUCTUATION / 2
    #     sigma1 = SIGMA1 + SIGMA1_FLUCTUATION * np.random.random() - SIGMA1_FLUCTUATION / 2
    #     mu2 = MU2 + MU2_FLUCTUATION * np.random.random() - MU2_FLUCTUATION / 2
    #     sigma2 = SIGMA2 + SIGMA2_FLUCTUATION * np.random.random() - SIGMA2_FLUCTUATION / 2
    #     uniform_collection = (supremum - infimum) * np.random.random_sample(
    #         COLLECTION_SIZE - GAUSSIAN_PROPORTION1 - GAUSSIAN_PROPORTION2
    #     ) + infimum
    #     gaussian_collection1 = np.random.normal(mu1, sigma1, GAUSSIAN_PROPORTION1)
    #     gaussian_collection2 = np.random.normal(mu2, sigma2, GAUSSIAN_PROPORTION2)
    #     collection = drift + np.concatenate((uniform_collection, gaussian_collection1, gaussian_collection2))
    #     output_file.write("%f" % collection[0])
    #     output_file.writelines("\t%f" % collection[i] for i in range(1, COLLECTION_SIZE))
    #     output_file.write('\n')
    # output_file.close()
    correct_data = loadCollectionFromFile("Synthetic/RandShapeCorrect.csv")
    anomalous_data = loadCollectionFromFile("Synthetic/RandShapeAnomalous.csv")
    for i in range(1, len(correct_data)):
        drift_value = drift_step * i
        for j in range(len(correct_data[i])):
            correct_data[i][j] += drift_value
            anomalous_data[i][j] += drift_value
    output_file = open("Synthetic/RandShapeWithDriftCorrect.csv", 'w')
    for collection in correct_data:
        output_file.write("%f" % collection[0])
        output_file.writelines("\t%f" % collection[i] for i in range(1, COLLECTION_SIZE))
        output_file.write('\n')
    output_file.close()
    output_file = open("Synthetic/RandShapeWithDriftAnomalous.csv", 'w')
    for collection in anomalous_data:
        output_file.write("%f" % collection[0])
        output_file.writelines("\t%f" % collection[i] for i in range(1, COLLECTION_SIZE))
        output_file.write('\n')
    output_file.close()

    print("Random-shape Distribution(with Drift) Generation Done.")


if __name__ == '__main__':
    COLLECTION_SIZE = 1000
    SAMPLE_SIZE = 1000
    DRIFT_STEP = 0.005
    # genUniform(COLLECTION_SIZE, SAMPLE_SIZE)
    # genGaussian(COLLECTION_SIZE, SAMPLE_SIZE)
    # genRandomShape(COLLECTION_SIZE, SAMPLE_SIZE)
    genRandomShapeDrifted(COLLECTION_SIZE, SAMPLE_SIZE, DRIFT_STEP)
