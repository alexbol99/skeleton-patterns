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

'''
    Input: data sorted by group label
    For each group with same label that has more than two rows:
        - sort group by coordinate on the line representing group
        - take first and last point in the group as start and end of the segment
        - add segment to dictionary under key l
'''
def extract_segments(data):
    l = None
    group = []
    segments = {}
    for row in data:
        label = row[4]
        if label != l:
            if len(group) > 2:
                group = sorted(group, key=lambda r: r[5])
                segments[l] = \
                    (group[0][0],group[0][1],group[-1][0],group[-1][1])

            group = []
            l = label

        s = point_to_coord(row[0],row[1],row[2],row[3])
        group.append(row + [s])

    return segments

def detect_segments(data):
    rho = [normal_to_angle(row[2], row[3]) for row in data]
    dist = [point_to_dist(row[0],row[1],row[2],row[3]) for row in data]

    X = list(zip(rho,dist))

    brc = Birch(branching_factor=50,n_clusters=None, threshold=0.5)
    rrr = brc.fit(X)
    labels = brc.predict(X)

    sorted_data = [row + [label] for (row,label) in zip(data,labels)]
    sorted_data = sorted(sorted_data, key=lambda row: row[4])

    segments = extract_segments(sorted_data)

    filtered_data = list(filter(lambda row: row[4] not in segments, sorted_data))
    filtered_data = [row[0:4] for row in filtered_data]

    return segments, filtered_data
