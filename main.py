from csv import reader

import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from script.enclosing_angles import get_enclosing_angle_and_border_degree, get_border_point, get_border_points, get_directional_angles
from script.k_nearest_neighbor import get_neighbors, get_mean_points

# cmap = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

# 1000 samples, k = 5 ### v2
# 6500 samples, k = 8 ### v3
# 500 samples, k = 5 ### v3 half
k = 5
beta = 0.1
n = 500
factor = beta * n


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

    print(f"directional angles: {angles}\n")

    dir_angles = [float(angle) for angle in angles]

    tmp_angles = []
    for angle in dir_angles:
        if angle >= 180:
            tmp_angles.append(angle)

    enc_angle = 360 - min(tmp_angles)

    print(f"enclosing angle: {enc_angle}\n\n")

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


def get_key(item):
    return item[3]


def extract_border_points(border_degree_point):
    print(f"factor: {factor}")
    border_points = []
    border_degree_point.sort(key=get_key, reverse=True)
    i = 0
    while i <= factor:
        for bdp in border_degree_point:
            print(f"i: {i}")
            print(f"border degree point: {bdp}")
            border_points.append([bdp[0], bdp[1]])
        i += 1
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
        for row in csv_reader:
            rows.append(row)
        knn = compute_knn(rows)
        mp = compute_mean_points(knn)
        # eak = compute_enclosing_angles_knn(rows, knn)
        # bp = find_border_points(eak, mp)
        # plot_results(rows, bp)
        # exit(0)
        dam = compute_directional_angles_mean_knn(rows, mp, knn)
        ea = compute_enclosing_angles_and_border_degree(dam)
        bdp = compute_border_points(ea)
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
    read_dataset('dataset/dataset_v3_half.csv')
    # trial_iris_dataset()
