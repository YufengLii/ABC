import numpy as np
from math import pi


def euclidean_distance(r1, r2):
    return np.sqrt(np.sum((r1 - r2) ** 2))


def get_direction(x1, y1, x2, y2):
    return [[round((float(x2) - float(x1)), 2), round((float(y2) - float(y1)), 2)], [int(x1), int(y1)]]


def scalar_product(x, y):
    return np.dot(x, y, None)


def module_vector(x, y):
    return np.sqrt(x ** 2 + y ** 2)


def angle_between_vectors(x1, y1, x2, y2):
    return scalar_product([x1, y1], [x2, y2]) / (module_vector(x1, y1) * module_vector(x2, y2))


def direction_angle_modified_distance_function(a, b):
    return euclidean_distance(np.asarray(a).astype(int), np.asarray(b).astype(int)) * (1 + ((0.5 - 1) / pi) * angle_between_vectors(a[0], a[1], b[0], b[1]))


"""
This is a simple implementation of DBSCAN intended to explain the algorithm.

@author: Chris McCormick
"""


def dbscan(dataset, eps, min_pts):
    """
    Cluster the dataset `D` using the DBSCAN algorithm.

    MyDBSCAN takes a dataset `D` (a list of vectors), a threshold distance
    `eps`, and a required number of points `MinPts`.

    It will return a list of cluster labels. The label -1 means noise, and then
    the clusters are numbered starting from 1.
    """

    # This list will hold the final cluster assignment for each point in D.
    # There are two reserved values:
    #    -1 - Indicates a noise point
    #     0 - Means the point hasn't been considered yet.
    # Initially all labels are 0.
    labels = [0] * len(dataset)

    # C is the ID of the current cluster.
    cluster_id = 0

    # This outer loop is just responsible for picking new seed points--a point
    # from which to grow a new cluster.
    # Once a valid seed point is found, a new cluster is created, and the
    # cluster growth is all handled by the 'expand_cluster' routine.

    # For each point P in the Dataset D...
    # ('P' is the index of the datapoint, rather than the datapoint itself.)
    for point in range(0, len(dataset)):
        # Only points that have not already been claimed can be picked as new
        # seed points.
        # If the point's label is not 0, continue to the next point.
        if not (labels[point] == 0):
            continue

        # Find all of P's neighboring points.
        neighbor_pts = region_query(dataset, point, eps)

        # If the number is below MinPts, this point is noise.
        # This is the only condition under which a point is labeled
        # NOISE--when it's not a valid seed point. A NOISE point may later
        # be picked up by another cluster as a boundary point (this is the only
        # condition under which a cluster label can change--from NOISE to
        # something else).
        if len(neighbor_pts) < min_pts:
            labels[point] = -1
        # Otherwise, if there are at least MinPts nearby, use this point as the
        # seed for a new cluster.
        else:
            cluster_id += 1
            grow_cluster(dataset, labels, point, neighbor_pts, cluster_id, eps, min_pts)

    # All data has been clustered!
    return labels


def grow_cluster(dataset, labels, point, neighbor_pts, cluster_id, eps, min_pts):
    """
    Grow a new cluster with label `C` from the seed point `P`.

    This function searches through the dataset to find all points that belong
    to this new cluster. When this function returns, cluster `C` is complete.

    Parameters:
      `D`      - The dataset (a list of vectors)
      `labels` - List storing the cluster labels for all dataset points
      `P`      - Index of the seed point for this new cluster
      `NeighborPts` - All the neighbors of `P`
      `C`      - The label for this new cluster.
      `eps`    - Threshold distance
      `MinPts` - Minimum required number of neighbors
    """

    # Assign the cluster label to the seed point.
    labels[point] = cluster_id

    # Look at each neighbor of P (neighbors are referred to as Pn).
    # NeighborPts will be used as a FIFO queue of points to search--that is, it
    # will grow as we discover new branch points for the cluster. The FIFO
    # behavior is accomplished by using a while-loop rather than a for-loop.
    # In NeighborPts, the points are represented by their index in the original
    # dataset.
    i = 0
    while i < len(neighbor_pts):
        # Get the next point from the queue.
        next_point = neighbor_pts[i]

        # If Pn was labelled NOISE during the seed search, then we
        # know it's not a branch point (it doesn't have enough neighbors), so
        # make it a leaf point of cluster C and move on.
        if labels[next_point] == -1:
            labels[next_point] = cluster_id

        # Otherwise, if Pn isn't already claimed, claim it as part of C.
        elif labels[next_point] == 0:
            # Add Pn to cluster C (Assign cluster label C).
            labels[next_point] = cluster_id

            # Find all the neighbors of Pn
            next_point_neighbor_pts = region_query(dataset, next_point, eps)

            # If Pn has at least MinPts neighbors, it's a branch point!
            # Add all of its neighbors to the FIFO queue to be searched.
            if len(next_point_neighbor_pts) >= min_pts:
                neighbor_pts = neighbor_pts + next_point_neighbor_pts
                neighbor_pts = list(dict.fromkeys(neighbor_pts))
            # If Pn *doesn't* have enough neighbors, then it's a leaf point.
            # Don't queue up it's neighbors as expansion points.
            # else:
            # Do nothing
            # NeighborPts = NeighborPts

        # Advance to the next point in the FIFO queue.
        i += 1

        # We've finished growing cluster C!


def region_query(dataset, point, eps):
    """
    Find all points in dataset `D` within distance `eps` of point `P`.

    This function calculates the distance between a point P and every other
    point in the dataset, and then returns only those points which are within a
    threshold distance `eps`.
    """
    neighbors = []

    # For each point in the dataset...
    for next_point in range(0, len(dataset)):
        # If the distance is below the threshold, add it to the neighbors list.
        # if np.linalg.norm(dataset[point] - dataset[next_point]) < eps:
        if direction_angle_modified_distance_function(dataset[point], dataset[next_point]) < eps:
            neighbors.append(next_point)

    return neighbors


def assign_non_border_points_to_cluster(rows, border_points, labels):
    points_labels = []
    for row in rows:
        point = [int(row[0]), int(row[1])]
        if not (point in border_points):
            distances = []
            labels_dis = []
            for bp in range(0, len(border_points)):
                if labels[bp] != -1:
                    distances.append(direction_angle_modified_distance_function(point, border_points[bp]))
                    labels_dis.append(labels[bp])
            min_distance = min(distances)
            for index in range(0, len(labels_dis)):
                if min_distance == distances[index]:
                    if labels_dis[index] == -1:
                        label_min = 0
                    else:
                        label_min = labels_dis[index]
                    break
            points_labels.append([point, label_min])
    return points_labels
