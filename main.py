from csv import reader
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.cluster import KMeans
from sklearn import datasets
from sklearn.model_selection import train_test_split

from script.k_nearest_neighbor import get_neighbors, get_mean_distances, get_mean_points
from script.enclosing_angles import get_enclosing_angle, get_enclosing_angles, get_border_degree_and_point

cmap = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

# 1000 samples, k = 5
k = 5
beta = 50
n = 1000
factor = beta * n


def plot_knn_and_mean_points(rows, knn, mp):
    x_all = []
    y_all = []
    for rw in rows:
        x_all.append(float(rw[0]))
        y_all.append(float(rw[1]))

    for i in range(len(rows)):
        plt.scatter(x_all, y_all, c='red', label='all', marker="o")

        x = [float(rows[i][0])]
        y = [float(rows[i][1])]
        plt.scatter(x, y, c='blue', label='center', marker="o")

        x_knn = []
        y_knn = []
        for point in knn[i]:
            x_knn.append(float(point[0]))
            y_knn.append(float(point[1]))
        plt.scatter(x_knn, y_knn, c='orange', label='knn', marker="o")

        x_mp = [float(mp[i][0])]
        y_mp = [float(mp[i][1])]
        plt.scatter(x_mp, y_mp, c='black', label='mp', marker="o")

        plt.legend()
        plt.grid(True)

        plt.show()


def plot_results(rows, bp):
    fig, ax = plt.subplots(2, figsize=(10, 8))
    x = []
    y = []
    for row in rows:
        x.append(float(row[0]))
        y.append(float(row[1]))

    xb = []
    yb = []
    for point in bp:
        xb.append(float(point[0]))
        yb.append(float(point[1]))

    ax[0].scatter(x, y, c='blue', label='all')
    ax[0].scatter(xb, yb, c='orange', label='border')
    ax[0].legend()
    ax[0].grid(True)

    model = KMeans(n_clusters=k)
    model.fit(rows)
    ax[1].scatter(x, y, c=model.labels_)

    plt.show()


def get_key(item):
    return item[2]


def extract_border_points(border_degree_point):
    border_points = []
    # print(border_degree_point)
    # print()
    # border_degree_point.sort(key=get_key, reverse=True)
    # print(border_degree_point)
    if len(border_degree_point) < factor:
        for i in range(len(border_degree_point)):
            border_points.append([border_degree_point[i][0], border_degree_point[i][1]])
    else:
        for i in range(beta):
            border_points.append([border_degree_point[i][0], border_degree_point[i][1]])
    # print(border_points)
    return border_points


def compute_border_degree(rows, enc_angles_mean_knn):
    border_degree_point = []
    for i in range(len(rows)):
        if get_border_degree_and_point(rows[i], enc_angles_mean_knn[i]) is not None:
            border_degree_point.append(get_border_degree_and_point(rows[i], enc_angles_mean_knn[i]))
    # print(border_degree_point)
    return border_degree_point


def compute_enclosing_angles(rows, knn):
    enc_angles = []
    for i in range(len(rows)):
        _index, enc_angle = get_enclosing_angle(rows[i], knn[i], k)
        enc_angles.append([_index, enc_angle])
    return enc_angles


def compute_enclosing_angles_mean_knn(rows, mp, knn):
    enc_angles = []
    for i in range(len(rows)):
        enc_angles.append(get_enclosing_angles(rows[i], mp[i], knn[i], k))
    return enc_angles


def compute_mean_points(knn):
    return get_mean_points(knn)


def compute_mean_distance(rows, knn):
    return get_mean_distances(rows, knn, k)


def compute_knn(rows):
    nearest_neighbors = []
    for r in rows:
        # print(r)
        neigh = get_neighbors(rows, r, k)
        # print(neigh)
        # print()
        # plot_knn(rows, r, neigh)
        nearest_neighbors.append(neigh)
    return nearest_neighbors


def read_dataset(path):
    with open(path, 'r') as dataset:
        csv_reader = reader(dataset)
        rows = []
        for row in csv_reader:
            rows.append(row)
        knn = compute_knn(rows)
        # md = compute_mean_distance(rows, knn)
        mp = compute_mean_points(knn)
        # ea = compute_enclosing_angles(rows, knn)
        eam = compute_enclosing_angles_mean_knn(rows, mp, knn)
        # plot_knn_and_mean_points(rows, knn, mp)
        bdp = compute_border_degree(rows, eam)
        bp = extract_border_points(bdp)
        plot_results(rows, bp)


# def trial_iris_dataset():
#     iris = datasets.load_iris()
#     X, y = iris.data, iris.target
#
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234)
#
#     # plt.figure()
#     # plt.scatter(X[:, 2], X[:, 3], c=y, cmap=cmap, edgecolors='k', s=20)
#     # plt.show()
#
#     clf = KNN(k=5)
#     clf.fit(X_train, y_train)
#     predictions = clf.predict(X_test)
#
#     acc = np.sum(predictions == y_test) / len(y_test)
#     print(acc)


if __name__ == '__main__':
    read_dataset('dataset/dataset_v2.csv')
    # trial_iris_dataset()

