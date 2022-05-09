from math import sqrt, dist
import numpy as np


def euclidean_distance(r1, r2):
    return np.sqrt(np.sum((r1 - r2) ** 2))


def get_neighbors(train, test_row, num_neighbors):
    distances = list()
    for train_row in train:
        distance = euclidean_distance(np.asarray(test_row).astype(int), np.asarray(train_row).astype(int))
        distances.append((train_row, distance))
    distances.sort(key=lambda tup: tup[1])
    distances = list(filter(lambda x: x[1] != 0.0, distances))
    neighbors = list()
    for i in range(num_neighbors):
        # print(distances[i][0])
        neighbors.append(distances[i][0])
    return neighbors


def get_mean_distances(rows, knn, k):
    mean_distances = []
    distances = []
    for i in range(len(rows)):
        point = (float(rows[i][0]), float(rows[i][1]))
        points_knn = []
        point_distances = []
        for p in knn[i]:
            points_knn.append((float(p[0]), float(p[1])))
        for p in points_knn:
            point_distances.append(dist(point, p))
        distances.append(point_distances)
        for d in distances:
            mean_distances.append((d[0] + d[1] + d[2]) / k)


def get_mean_points(knn):
    mean_points = []
    for nn in knn:
        x = 0
        y = 0
        for i in range(len(nn)):
            x += float(nn[i][0])
            y += float(nn[i][1])
        mean_x = x / len(nn)
        mean_y = y / len(nn)
        mean_points.append([mean_x, mean_y])
    return mean_points


# class KNN:
#     def __init__(self, k=3):
#         self.X_train = None
#         self.y_train = None
#         self.k = k
#
#     # X training samples, y training labels
#     def fit(self, X, y):
#         self.X_train = X
#         self.y_train = y
#
#     # X test samples
#     def predict(self, X):
#         predicted_labels = [self._predict(x) for x in X]
#         return np.array(predicted_labels)
#
#     def _predict(self, x):
#         # compute distances
#         distances = [euclidean_distance(x, x_train) for x_train in self.X_train]
#         # get k nearest samples, labels
#         k_indices = np.argsort(distances)[:self.k]
#         k_nearest_labels = [self.y_train[i] for i in k_indices]
#         # majority vote, get the most common class label
#         most_common = Counter(k_nearest_labels).most_common(1)
#         return most_common[0][0]
