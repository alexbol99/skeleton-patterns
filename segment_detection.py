import math
from sklearn.cluster import Birch

def normal_to_angle(x,y):
    alpha = math.atan2(y,x)
    if alpha < 0:
        alpha += 2*math.pi
    return alpha

def point_to_dist(px,py,nx,ny):
    return math.fabs(px*nx + py*ny)

def point_to_coord(px,py,nx,ny):
    return nx*py - ny*px

def extract_segments(data):
    l = None
    group = []
    segments = []
    for row in data:
        label = row[4]
        if label != l:
            if len(group) > 2:
                group = sorted(group, key=lambda r: r[5])
                segments.append(
                    (group[0][0],group[0][1],group[-1][0],group[-1][1])
                )
            group = []
            l = label

        s = point_to_coord(row[0],row[1],row[2],row[3])
        group.append(row + [s])

    return segments

def detect_segments(data):
    rho = [normal_to_angle(row[2], row[3]) for row in data]
    dist = [point_to_dist(row[0],row[1],row[2],row[3]) for row in data]

    X = [(r,d) for (r,d) in zip(rho,dist)]

    brc = Birch(branching_factor=50,n_clusters=None, threshold=0.5)
    rrr = brc.fit(X)
    labels = brc.predict(X)

    sorted_data = [row + [label] for (row,label) in zip(data,labels)]
    sorted_data = sorted(sorted_data, key=lambda row: row[4])

    segments = extract_segments(sorted_data)
    return segments
