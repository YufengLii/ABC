from csv import reader
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

from script.k_nearest_neighbor import get_neighbors, get_mean_distances, get_mean_points
from script.enclosing_angles import get_enclosing_angle, get_enclosing_angles, get_border_degree_and_point

# 3000 samples
k = 10
beta = 300


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
    border_degree_point.sort(key=get_key, reverse=True)
    for i in range(beta):
        border_points.append([border_degree_point[i][0], border_degree_point[i][1]])
    # print(border_points)
    return border_points


def compute_border_degree(rows, enc_angles_mean_knn):
    border_degree_point = []
    for i in range(len(rows)):
        border_degree_point.append(get_border_degree_and_point(rows[i], enc_angles_mean_knn[i]))
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
        nearest_neighbors.append(get_neighbors(rows, r, k))
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
        bdp = compute_border_degree(rows, eam)
        bp = extract_border_points(bdp)
        plot_results(rows, bp)


if __name__ == '__main__':
    read_dataset('dataset/dataset.csv')
