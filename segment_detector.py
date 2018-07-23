'''
    Detect segments using BIRCH classification (https://en.wikipedia.org/wiki/BIRCH)
    BIRCH == Balanced Iterative Reducing and Clustering using Hierarchies
    Input:
        data - table of medial points and normal vectors
    Output:
        segments - dictionary of detected, key is the label of the group after BIRCH
        data_filtered - data which do not belong to groups
    Algorithm:
        1. transform (point,normal) to (rho, dist) coordinate system
        2. classify (rho, dist) points and assign label to each row
        3. sort by label
        4. each group with same label represent a line, extract segment from group
        5. collect segments into dictionary, return segments
        6. filter input data and return rows that are not classified
    TODO: split segment if there is a gap between points more than given parameter
'''
import math
from sklearn.cluster import Birch
# from sklearn.cluster import MeanShift, estimate_bandwidth
import numpy as np
from parameters import *

'''
    Slope of the normal vector
'''
def normal_to_angle(x,y):
    alpha = math.atan2(y,x)
    if alpha < 0:
        alpha += 2*math.pi
    return alpha

def sp(px,py,nx,ny):
    return px*nx + py*ny

def unit_vector(x,y):
    len = math.sqrt(x**2 + y**2)
    return x/len,y/len

def point_to_ref(px,py,nx,ny):
    signed_dist = sp(px,py,nx,ny)
    return signed_dist*nx,signed_dist*ny

'''
    Distance from (0,0) to the line passed through point p(x,y) with the normal n(x,y)
'''
def point_to_dist(px,py,nx,ny):
    return math.fabs(px*nx + py*ny)

'''
    Coordinate on line passed through point p(x,y) with the normal n(x,y)
'''
def point_to_coord(px,py,nx,ny):
    return nx*py - ny*px

'''
    Distance between two points (x1,y1) and (x2,y2)
'''
def length(x1, y1, x2, y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

'''
    Projection from point (x,y) on the line (px,py,nx,ny)
'''
def projection_on_line(x,y,px,py,nx,ny):
    vecX = px - x
    vecY = py - y
    dist = vecX*nx + vecY*ny       # dot product vec * n, signed
    prjX = x + dist*nx
    prjY = y + dist*ny
    return prjX, prjY

def group_to_segments(group):
    segments = []
    startX = group[0][0]
    startY = group[0][1]
    endX = group[-1][0]
    endY = group[-1][1]
    n = len(group)
    segment = [startX, startY, endX, endY]
    for i in range(n-1):
        row = group[i]
        next_row = group[i+1]
        length = math.sqrt((next_row[0]-row[0])**2 + (next_row[1]-row[1])**2)
        if length > SEGMENT_DETECTOR_MAX_GAP_IN_GROUP:
            segments.append([segment[0],segment[1],row[0],row[1]])

            segment[0] = next_row[0]          # set next segment startX coordinate
            segment[1] = next_row[1]          # set next segment startY coordinate

    # add last segment
    segments.append([segment[0],segment[1],segment[2],segment[3]])

    return segments

'''
    Input: data sorted by group label
    For each group with same label that has more than two rows:
        - sort group by coordinate on the line representing group
        - take first and last point in the group as start and end of the segment
        - add segment to dictionary under key l
'''
def extract_segments(data, cluster_centers):
    l = None
    group = []
    segments = {}
    for row in data:
        label = row[4]
        if label != l:
            if len(group) > SEGMENT_DETECTOR_MIN_IN_GROUP:
                group = sorted(group, key=lambda r: r[5])
                segments[l] = group_to_segments(group)
                # segments[l] = \
                #     (group[0][0],group[0][1],group[-1][0],group[-1][1])

            group = []
            l = label

        subcluster_center = cluster_centers[label]
        # =========================================
        # rho, distance
        angle = subcluster_center[0]
        dist = subcluster_center[1]
        nx = math.cos(angle)
        ny = math.sin(angle)
        px = dist*nx
        py = dist*ny

        # =========================================
        # reference vector
        # nx,ny = unit_vector(subcluster_center[0], subcluster_center[1])
        # px = subcluster_center[0]
        # py = subcluster_center[1]

        # prjX, prjY = projection_on_line(row[0], row[1], px, py, nx, ny)

        # s = point_to_coord(row[0],row[1],row[2],row[3])
        s = point_to_coord(row[0], row[1], nx, ny)

        # length = math.sqrt( (prjX - row[0])**2 + (prjY - row[1])**2 )
        # if length < 1:

        # s = point_to_coord(prjX, prjY, nx, ny)

        group.append(row + [s])
    else:
        if len(group) > SEGMENT_DETECTOR_MIN_IN_GROUP:
            group = sorted(group, key=lambda r: r[5])
            segments[l] = group_to_segments(group)
            # segments[l] = \
            #     (group[0][0], group[0][1], group[-1][0], group[-1][1])

    return segments

def detect_segments(data):
    rho = [normal_to_angle(row[2], row[3]) for row in data]
    dist = [point_to_dist(row[0],row[1],row[2],row[3]) for row in data]

    X = list(zip(rho,dist))
    ############### X = np.array(X)

    # X = [point_to_ref(row[0],row[1],row[2],row[3]) for row in data]

    brc = Birch(branching_factor=50,n_clusters=None, threshold=SEGMENT_DETECTOR_BIRCH_THRESHOLD)
    rrr = brc.fit(X)
    labels = brc.predict(X)
    cluster_centers = brc.subcluster_centers_

    # bandwidth = estimate_bandwidth(X, quantile=0.2, n_samples=500)
    # ms = MeanShift(bandwidth, bin_seeding=True)
    # ms.fit(X)
    # labels = ms.labels_
    # cluster_centers = ms.cluster_centers_

    sorted_data = [row + [label] for (row,label) in zip(data,labels)]
    sorted_data = sorted(sorted_data, key=lambda row: row[4])

    # indices = [index for index in range(len(labels)) if labels[index] == 1243]
    # sorted_data = list(filter(lambda row: row[4] == 286, sorted_data))

    segments = extract_segments(sorted_data, cluster_centers)

    # filtered_data = sorted_data

    filtered_data = list(filter(lambda row: row[4] not in segments, sorted_data))
    filtered_data = [row[0:4] for row in filtered_data]

    output_segments = []
    for label, list_of_segments in segments.items():
        [output_segments.append(segment + [str(label)]) for segment in list_of_segments]

    return output_segments, filtered_data
