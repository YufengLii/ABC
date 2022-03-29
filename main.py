from csv import reader
from script.k_nearest_neighbor import get_neighbors, get_mean_distances, get_mean_points
from script.enclosing_angles import get_enclosing_angle, get_enclosing_angles, get_border_degree_and_point

k = 3
beta = 50


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
        print(bdp)


if __name__ == '__main__':
    read_dataset('dataset/dataset.csv')
