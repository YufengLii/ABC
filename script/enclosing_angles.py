from math import atan2, degrees


def get_enc_angle(x, y, z):
    u1, u2 = y[0] - x[0], y[1] - x[1]  # xy coordinates
    v1, v2 = z[0] - x[0], z[1] - x[1]  # xz coordinates
    enclosing_angle = atan2(u2, u1) - atan2(v2, v1)
    deg_enclosing_angle = degrees(enclosing_angle)
    if deg_enclosing_angle < 0:
        return 360 - (deg_enclosing_angle + 360)
    else:
        return 360 - deg_enclosing_angle


def get_enclosing_angle(point, knn, k):
    # print(point)
    # print(knn)
    enc_angles_point = []
    for j in range(k):
        for g in reversed(range(k)):
            if j != g and g <= k - 1:
                enc_angles_point.append(get_enc_angle([float(point[0]), float(point[1])],
                                                      [float(knn[j][0]), float(knn[j][1])],
                                                      [float(knn[g][0]), float(knn[g][1])]))
            else:
                break
    # print(enc_angles_point)
    # print()
    enc_angle_point = max(enc_angles_point)
    index_enc_angle = enc_angles_point.index(max(enc_angles_point))
    return index_enc_angle, enc_angle_point


def get_enclosing_angles(point, mean_point, knn, k):
    enc_angles_point = []
    for j in range(k):
        enc_angle_point = (get_enc_angle([float(point[0]), float(point[1])],
                                         [float(mean_point[0]), float(mean_point[1])],
                                         [float(knn[j][0]), float(knn[j][1])]))
        enc_angles_point.append(enc_angle_point)
    return enc_angles_point


def get_border_degree_and_point(row, enc_angles):
    enc_angles.sort(reverse=True)
    # print(enc_angles)
    if enc_angles[0] < 270:
        print(enc_angles[0])
        return [row[0], row[1], enc_angles[0]]
