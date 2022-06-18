from math import atan2, degrees


def get_dir_angle(center, mean_point, nn):
    u1, u2 = mean_point[0] - center[0], mean_point[1] - center[1]  # center-mean_point coordinates (mean_point - center)
    v1, v2 = nn[0] - center[0], nn[1] - center[1]  # center-nn coordinates (nn - center)
    directional_angle = atan2(v2, v1) - atan2(u2, u1)  # center-nn - center-mean_point
    deg_directional_angle = degrees(directional_angle)

    if deg_directional_angle < 0:
        deg_directional_angle += 360

    return float(deg_directional_angle)


def get_directional_angles(point, mean_point, knn, k):
    dir_angles_point = []
    for j in range(k):
        dir_angle_point = (get_dir_angle([float(point[0]), float(point[1])],
                                         [float(mean_point[0]), float(mean_point[1])],
                                         [float(knn[j][0]), float(knn[j][1])]))
        dir_angles_point.append(dir_angle_point)
    return dir_angles_point


# def get_enclosing_angles_knn(point, knn):
#     x1 = 0
#     y1 = 0
#     x2 = 0
#     y2 = 0
#     enc_angles_points = []
#     enc_angles = []
#     len_loop = range(len(knn))
#     for i in len_loop:
#         dir_angles = []
#         dir_angles_points = []
#         for j in len_loop:
#             if i != j:
#                 dir_angles.append(get_dir_angle([float(point[0]), float(point[1])],
#                                                 [float(knn[i][0]), float(knn[i][1])],
#                                                 [float(knn[j][0]), float(knn[j][1])]))
#                 dir_angles_points.append([get_dir_angle([float(point[0]), float(point[1])],
#                                                         [float(knn[i][0]), float(knn[i][1])],
#                                                         [float(knn[j][0]), float(knn[j][1])]),
#                                           [float(knn[i][0]), float(knn[i][1])],
#                                           [float(knn[j][0]), float(knn[j][1])]])
#         enc_angles.append(get_enclosing_angle_knn(dir_angles))
#         enc_angles_points.append([get_enclosing_angle_knn(dir_angles), find_points_enc_angle(dir_angles, dir_angles_points)])
#
#     max_enc_angle = max(enc_angles)
#     for eap in enc_angles_points:
#         if eap[0] == max_enc_angle:
#             x1 = eap[1][0][0]
#             y1 = eap[1][0][1]
#             x2 = eap[1][1][0]
#             y2 = eap[1][1][1]
#
#     return float(point[0]), float(point[1]), x1, y1, x2, y2, max_enc_angle


def get_enclosing_angle_and_border_degree(x, y, angles):
    dir_angles = [float(angle) for angle in angles]

    tmp_angles = []
    for angle in dir_angles:
        if angle >= 180:
            tmp_angles.append(angle)

    enc_angle = 360 - min(tmp_angles)
    border_degree = 360 - min(dir_angles)
    return [x, y, enc_angle, border_degree]


# def get_enclosing_angle_knn(angles):
#     dir_angles = [float(angle) for angle in angles]
#     enc_angle = 360 - min(dir_angles)
#     return float(enc_angle)


# def find_points_enc_angle(dir_angles, dir_angles_point):
#     angles = [float(dir_angle) for dir_angle in dir_angles]
#     min_dir_angle = min(angles)
#     for dap in dir_angles_point:
#         if dap[0] == min_dir_angle:
#             return dap[1], dap[2]


def get_border_points(angles_points, mean_points):
    # for i in range(len(angles_points)):
    #     print(angles_points[i])
    #     print(mean_points[i])
    #     dir_angle = get_dir_angle([angles_points[i][0], angles_points[i][1]],
    #                               [mean_points[i][0], mean_points[i][1]],
    #                               [angles_points[i][4], angles_points[i][5]])
    #     print(dir_angle)
    #     print()
    # exit(0)

    border_points = []
    for ap in angles_points:
        # print(f"angle point: {ap}\n")
        if 0 <= ap[6] < 135:
            border_points.append(ap[2])
    return border_points


def get_border_point(enc_angles_point):
    # for point in enc_angles_point:
    #    print(f"point + angles: {point}\n\n")
    enc_angles = []
    for enc_angle in enc_angles_point:
        enc_angles.append(enc_angle[2])
    border_point_angle = []
    angles = [float(angle) for angle in enc_angles]
    for i in range(len(angles)):
        if angles[i] < 60:
            border_point_angle.append([enc_angles_point[i][0], enc_angles_point[i][1], angles[i], enc_angles_point[i][3]])
    return border_point_angle
