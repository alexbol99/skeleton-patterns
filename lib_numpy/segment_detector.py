'''
    Detect segments using BIRCH classification
    Input:
        data - table of points and normal to expected segment in each point
    Output:
        segments - dictionary of detected, key is the label of the group after BIRCH
        data_filtered - data which do not belong to groups
    Algorithm:
        - transform (point,normal) to (rho, dist) coordinate system
        - classify (rho, dist) points and assign label to each row
        - sort by label
        - each group with same label represent a line, extract segment from group
        - collect segments into dictionary, return segments
        - filter input data and return rows that are not classified
    TODO: split segment if there is a gap between points more than given parameter
'''
import numpy as np
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
        group.append(list(row) + [s])
        # group.append(np.concatenate((row, np.array[s])))

    return segments

def detect_segments(data):
    # rho = [normal_to_angle(row[2], row[3]) for row in data]
    rho = np.arctan2(data[:,3],data[:,2])
    rho[rho < 0] += 2*math.pi
    #dist = [point_to_dist(row[0],row[1],row[2],row[3]) for row in data]
    dist = np.fabs(data[:,0]*data[:,2] + data[:,1]*data[:,3])

    # X = [(r,d) for (r,d) in zip(rho,dist)]
    X = list(zip(rho,dist))

    brc = Birch(branching_factor=50,n_clusters=None, threshold=0.5)
    rrr = brc.fit(X)
    labels = brc.predict(X)

    # sorted_data = [row + [label] for (row,label) in zip(data,labels)]
    # sorted_data = np.concatenate((data,np.array([labels],dtype=float).T),axis=1)
    sorted_data = np.zeros((data.shape[0],data.shape[1]+1))
    sorted_data[:,0:4] = data
    sorted_data[:,4:5] = np.array([labels],dtype=float).T

    # sorted_data = sorted(sorted_data, key=lambda row: row[4])
    sorted_data = sorted_data[sorted_data[:,4].argsort()]

    segments = extract_segments(sorted_data)

    filtered_data = list(filter(lambda row: row[4] not in segments, sorted_data))

    return segments, filtered_data


