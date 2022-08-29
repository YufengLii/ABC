from csv import reader

import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans

from script.enclosing_angles import get_enclosing_angle_and_border_degree, get_border_point, get_border_points, \
    get_directional_angles
from script.k_nearest_neighbor import get_neighbors, get_mean_points
from script.dbscan_modified import dbscan, assign_non_border_points_to_cluster

# cmap = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

# 1000 samples, k = 5 ### v2
# 6000 samples, k = 3 ### v3
# 500 samples, k = 5 ### v3 half
k = 12
beta = 0.2
n = 500
factor = int(beta * n)
f = open("results.txt", "w")


def plot_directional_angle(rows, row, mean_point, knn, angles):
    x_all = []
    y_all = []
    for rw in rows:
        x_all.append(float(rw[0]))
        y_all.append(float(rw[1]))
    plt.scatter(x_all, y_all, c='red', label='all', marker="o")

    x = [float(row[0])]
    y = [float(row[1])]
    plt.scatter(x, y, c='blue', label='center', marker="o")

    x_mp = [float(mean_point[0])]
    y_mp = [float(mean_point[1])]
    plt.scatter(x_mp, y_mp, c='black', label='mean point', marker="o")

    for index, point in enumerate(knn):
        plt.scatter(float(point[0]), float(point[1]), c='orange', label='knn', marker="o")
        plt.text(float(point[0]), float(point[1]), index)

    print(f"\n\ndirectional angles: {angles}")

    dir_angles = [float(angle) for angle in angles]

    tmp_angles = []
    for angle in dir_angles:
        if angle >= 180:
            tmp_angles.append(angle)

    enc_angle = 360 - min(tmp_angles)

    print(f"enclosing angle: {enc_angle}")

    border_degree = 360 - min(dir_angles)

    print(f"border degree: {border_degree}")

    plt.legend()
    plt.grid(True)

    plt.show()


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


def plot_clusters(rows, border_points, labels):
    new_labels = []
    for label in labels:
        if label == -1:
            new_labels.append(0)
        else:
            new_labels.append(label)

    scatter_x = []
    scatter_y = []
    for border_point in border_points:
        scatter_x.append(border_point[0])
        scatter_y.append(border_point[1])

    cdict = {1: 'yellow', 2: 'cyan', 3: 'green', 4: 'magenta', 5: 'red', 0: 'black'}

    fig, ax = plt.subplots()
    x_all = []
    y_all = []
    for row in rows:
        x_all.append(row[0])
        y_all.append(row[1])
    ax.scatter(x_all, y_all, c='blue', label='all')

    for label in np.unique(new_labels):
        indexes = []
        for i in range(0, len(new_labels)):
            if new_labels[i] == label:
                indexes.append(i)
        for index in indexes:
            ax.scatter(scatter_x[index], scatter_y[index], c=cdict[label])

    plt.show()


def plot_final_clusters(points_labels, border_points, labels):
    new_labels = []
    for label in labels:
        if label == -1:
            new_labels.append(0)
        else:
            new_labels.append(label)

    scatter_x = []
    scatter_y = []
    for border_point in border_points:
        scatter_x.append(border_point[0])
        scatter_y.append(border_point[1])

    other_scatter_x = []
    other_scatter_y = []
    for point_label in points_labels:
        other_scatter_x.append(point_label[0][0])
        other_scatter_y.append(point_label[0][1])

    cdict = {1: 'yellow', 2: 'cyan', 3: 'green', 4: 'magenta', 5: 'red', 0: 'black'}

    fig, ax = plt.subplots()
    for label in np.unique(new_labels):
        indexes = []
        for i in range(0, len(new_labels)):
            if new_labels[i] == label:
                indexes.append(i)
        for index in indexes:
            ax.scatter(scatter_x[index], scatter_y[index], c=cdict[label])
        other_indexes = []
        for j in range(0, len(points_labels)):
            if points_labels[j][1] == label:
                other_indexes.append(j)
        for other_index in other_indexes:
            ax.scatter(other_scatter_x[other_index], other_scatter_y[other_index], c=cdict[label])

    plt.show()


# def compute_directions_border_points(rows, mean_points, border_points):
#     directions_points = []
#     for bp in border_points:
#         for index, row in enumerate(rows):
#             if bp[0] == row[0] and bp[1] == row[1]:
#                 directions_points.append(get_direction(bp[0], bp[1],
#                                                        mean_points[index][0],
#                                                        mean_points[index][1]))
#     return directions_points


def get_key(item):
    return item[3]


def extract_border_points(border_degree_point):
    # print(f"factor: {factor}")
    border_points = []
    border_degree_point.sort(key=get_key, reverse=True)
    del border_degree_point[factor:]

    for bdp in border_degree_point:
        border_points.append([int(bdp[0]), int(bdp[1])])
    return border_points


def compute_border_points(enc_angles_mean_knn):
    border_points = get_border_point(enc_angles_mean_knn)
    return border_points


def compute_enclosing_angles_and_border_degree(directional_angles):
    enc_angles_border_degree = []
    for da in directional_angles:
        enc_angles_border_degree.append(get_enclosing_angle_and_border_degree(da[0], da[1], da[2]))
    return enc_angles_border_degree


def compute_directional_angles_mean_knn(rows, mp, knn):
    dir_angles = []
    for i in range(len(rows)):
        dir_angle = get_directional_angles(rows[i], mp[i], knn[i], k)
        dir_angles.append([rows[i][0], rows[i][1], dir_angle])
        # plot_directional_angle(rows, rows[i], mp[i], knn[i], dir_angle)
    return dir_angles


# def compute_enclosing_angles_knn(rows, knn):
#     enc_angles = []
#     for i in range(len(rows)):
#         curr_x, curr_y, x1, y1, x2, y2, angle = get_enclosing_angles_knn(rows[i], knn[i])
#         enc_angles.append([curr_x, curr_y, x1, y1, x2, y2, angle])
#     return enc_angles


def find_border_points(enc_angles_points, mean_points):
    return get_border_points(enc_angles_points, mean_points)


def compute_mean_points(knn):
    return get_mean_points(knn)


def compute_knn(rows):
    nearest_neighbors = []
    for r in rows:
        neigh = get_neighbors(rows, r, k)
        nearest_neighbors.append(neigh)
    return nearest_neighbors


def read_dataset(path):
    with open(path, 'r') as dataset:
        csv_reader = reader(dataset)
        rows = []
        f.write('Points:\n')
        for row in csv_reader:
            rows.append(row)
            f.write(str(row) + '\n')
        f.write('\n\nKNN:\n')
        knn = compute_knn(rows)
        for single_knn in knn:
            f.write(str(single_knn) + '\n')
        f.write('\n\nMean Points:\n')
        mean_points = compute_mean_points(knn)
        for mean_point in mean_points:
            f.write(str(mean_point) + '\n')
        # eak = compute_enclosing_angles_knn(rows, knn)
        # bp = find_border_points(eak, mp)
        # plot_results(rows, bp)
        # exit(0)
        f.write('\n\nDirectional Angles of Mean Point:\n')
        directional_angles_mean = compute_directional_angles_mean_knn(rows, mean_points, knn)
        for directional_angle_mean in directional_angles_mean:
            f.write(str(directional_angle_mean) + '\n')
        f.write('\n\nEnclosing Angles:\n')
        enclosing_angles = compute_enclosing_angles_and_border_degree(directional_angles_mean)
        for enclosing_angle in enclosing_angles:
            f.write(str(enclosing_angle) + '\n')
        f.write('\n\nAll Border Points:\n')
        border_points_all = compute_border_points(enclosing_angles)
        for border_point_all in border_points_all:
            f.write(str(border_point_all) + '\n')
        f.write('\n\nBorder Points:\n')
        border_points = extract_border_points(border_points_all)
        for border_point in border_points:
            f.write(str(border_point) + '\n')
        # plot_results(rows, border_points)
        f.write('\n\nLabels:\n')
        labels = dbscan(border_points, 18000, 3)
        for label in labels:
            f.write(str(label) + '\n')
        # plot_clusters(rows, border_points, labels)
        f.write('\n\nPoint Labels:\n')
        points_labels = assign_non_border_points_to_cluster(rows, border_points, labels)
        for point_labels in points_labels:
            f.write(str(point_labels) + '\n')
        plot_final_clusters(points_labels, border_points, labels)


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
    read_dataset('dataset/dataset_v3_half.csv')
    # trial_iris_dataset()
