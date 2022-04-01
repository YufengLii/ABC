from math import atan2, degrees


def get_directional_angle(x, y, z):
    u1, u2 = y[0] - x[0], y[1] - x[1]  # xy coordinates
    v1, v2 = z[0] - x[0], z[1] - x[1]  # xz coordinates
    directional_angle = atan2(u2, u1) - atan2(v2, v1)
    deg_directional_angle = degrees(directional_angle)
    if deg_directional_angle < 0:
        return deg_directional_angle + 360
    else:
        return deg_directional_angle


def get_enclosing_angle(point, knn, k):
    dir_angles_point = []
    for j in range(k):
        for g in reversed(range(k)):
            if j != g and g <= k - 1:
                dir_angles_point.append(get_directional_angle([float(point[0]), float(point[1])], [float(knn[j][0]), float(knn[j][1])], [float(knn[g][0]), float(knn[g][1])]))
            else:
                break
    min_dir_angle = min(dir_angles_point)
    index_min_dir_angle = dir_angles_point.index(min(dir_angles_point))
    enc_angle_point = 360 - min_dir_angle
    return index_min_dir_angle, enc_angle_point


def get_enclosing_angles(point, mean_point, knn, k):
    enc_angles_point = []
    for j in range(k):
        dir_angle_point = (get_directional_angle([float(point[0]), float(point[1])], [float(mean_point[0]), float(mean_point[1])], [float(knn[j][0]), float(knn[j][1])]))
        enc_angle_point = 360 - dir_angle_point
        enc_angles_point.append(enc_angle_point)
    # print(enc_angles_point)
    # print()
    return enc_angles_point


def get_border_degree_and_point(row, enc_angles):
    enc_angles.sort(reverse=True)
    return [row[0], row[1], enc_angles[0]]
