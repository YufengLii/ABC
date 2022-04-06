from math import sqrt, dist


def euclidean_distance(r1, r2):
    distance = 0.0
    for i in range(len(r1) - 1):
        distance += (int(float(r1[i])) - int(float(r2[i]))) ** 2
    return sqrt(distance)


def get_neighbors(train, test_row, num_neighbors):
    distances = list()
    for train_row in train:
        distance = euclidean_distance(test_row, train_row)
        distances.append((train_row, distance))
    distances.sort(key=lambda tup: tup[1])
    distances = list(filter(lambda x: x[1] != 0.0, distances))
    neighbors = list()
    for i in range(num_neighbors):
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
        x = x / len(nn)
        y = y / len(nn)
        mean_points.append([x, y])
    return mean_points
