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
# import numpy as np
from parameters import *

'''
    Slope of the normal vector
'''
def normal_to_angle(x,y):
    alpha = math.atan2(y,x)
    if alpha < 0:
        alpha += 2*math.pi
    return alpha

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
            segment[2] = row[0]               # set segment endX coordinate
            segment[3] = row[1]               # set segment endY coordinate
            segments.append(segment)

            segment[0] = next_row[0]          # set next segment startX coordinate
            segment[1] = next_row[1]          # set next segment startY coordinate

    # add last segment
    segments.append(segment)

    return segments

'''
    Input: data sorted by group label
    For each group with same label that has more than two rows:
        - sort group by coordinate on the line representing group
        - take first and last point in the group as start and end of the segment
        - add segment to dictionary under key l
'''
def extract_segments(data, brc):
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

        subcluster_center = brc.subcluster_centers_[label]
        angle = subcluster_center[0]
        # s = point_to_coord(row[0],row[1],row[2],row[3])
        s = point_to_coord(row[0], row[1], math.cos(angle), math.sin(angle))
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
    # X = np.array(X)

    brc = Birch(branching_factor=50,n_clusters=None, threshold=SEGMENT_DETECTOR_BIRCH_THRESHOLD)
    rrr = brc.fit(X)
    labels = brc.predict(X)

    sorted_data = [row + [label] for (row,label) in zip(data,labels)]
    sorted_data = sorted(sorted_data, key=lambda row: row[4])

    # indices = [index for index in range(len(labels)) if labels[index] == 1243]
    # sorted_data = list(filter(lambda row: row[4] == 1243, sorted_data))

    segments = extract_segments(sorted_data, brc)

    # filtered_data = sorted_data
    filtered_data = list(filter(lambda row: row[4] not in segments, sorted_data))
    filtered_data = [row[0:4] for row in filtered_data]

    output_segments = []
    for list_of_segments in segments.values():
        [output_segments.append(segment) for segment in list_of_segments]

    return output_segments, filtered_data
