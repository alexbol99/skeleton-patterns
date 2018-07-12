'''
    Arc detector
    Input:
        data - table of medial points and normal vectors, filtered after segment detection
    Output:
        arcs - dictionary of arcs detected, key is the label of the group after BIRCH
        data_filtered - data which do not belong to groups
    Algorithm:
        1. Connect points into sparse graph using k-nearest neighbors algorithm
        2. Remove redundant egdes by minimal spanning tree algorithm
        3. Using edges from MST graph create circle candidate (center, radius) for each point
        4. Classify circle candidates using BIRCH algorithm
        5. Create arc for each group more than 10 members using group centroid stored in BRC object
        6. Return circles as dictionary with key = group label
'''

# import matplotlib.pyplot as plt
import numpy as np
import math
from sklearn.cluster import Birch
from sklearn.neighbors import kneighbors_graph
from scipy.sparse.csgraph import minimum_spanning_tree
# from matplotlib.patches import Arc

def line_to_standard(px,py,nx,ny):
    A = nx
    B = ny
    C = nx*px + ny*py
    return A,B,C

def line_to_line_intersect(row1, row2):
    A1,B1,C1 = line_to_standard(row1[0],row1[1],row1[3],-row1[2])
    A2,B2,C2 = line_to_standard(row2[0],row2[1],row2[3],-row2[2])

    # Cramer's rule
    det = A1 * B2 - B1 * A2
    detX = C1 * B2 - B1 * C2
    detY = A1 * C2 - C1 * A2

    ip = [];
    if (det != 0):
        ip = [detX/det, detY/det]

    return ip

def length(x1,y1,x2,y2):
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def find_candidate_circles(data, p1, p2):
    Z = []
    for i,j in zip(p1,p2):
        ip = line_to_line_intersect(data[i], data[j])
        if (len(ip) > 0):
            r = length(ip[0],ip[1],data[i][0],data[i][1])
            Z.append([ip[0],ip[1],r])
    return Z

def point_to_slope(x,y,pcx,pcy):
    slope = math.atan2(y-pcy, x-pcx)
    if slope < 0:
        slope += 2*math.pi
    return slope

def define_angles(angles):
    start_angle = min(angles)
    end_angle = max(angles)
    return math.degrees(start_angle),math.degrees(end_angle)

def extract_arcs(data,brc):
    l = None
    group = []
    arcs = {}
    for row in data:
        label = row[4]
        if label != l:
            if len(group) > 10:
                # Sort by slope
                group = sorted(group, key=lambda r: r[8])
                start_angle,end_angle = define_angles([r[8] for r in group])
                arcs[l] = [(group[0][5],group[0][6]),group[0][7],start_angle,end_angle]

            group = []
            l = label

        subcluster_center = brc.subcluster_centers_[label]
        centerX = subcluster_center[0]
        centerY = subcluster_center[1]
        radius = subcluster_center[2]
        slope = point_to_slope(row[0],row[1],centerX, centerY)
        group.append(row + [centerX,centerY,radius,slope])

    return arcs

def detect_arcs(data):
    # generate a sparse graph using the k nearest neighbors of each point
    G = kneighbors_graph(data, n_neighbors=10, mode='distance')

    # Compute the minimum spanning tree of this graph
    MST = minimum_spanning_tree(G, overwrite=True)

    # Get the x, y coordinates of the beginning and end of each line segment
    T = MST.tocoo()

    # Filter edges where length > 10
    R = np.where(T.data < 10,T.row,-1)
    p1 = R[R>=0]
    C = np.where(T.data < 10,T.col,-1)
    p2 = C[C>=0]

    # Find candidate circles [(pcx,pcy,r)]
    Z = find_candidate_circles(data, p1, p2)

    # Classify candidate circles
    brc = Birch(branching_factor=50,n_clusters=None, threshold=0.5)
    res = brc.fit(Z)
    labels = brc.predict(Z)

    sorted_data = [row + [label] for (row,label) in zip(data,labels)]
    sorted_data = sorted(sorted_data, key=lambda row: row[4])

    arcs = extract_arcs(sorted_data, brc)

    filtered_data = list(filter(lambda row: row[4] not in arcs, sorted_data))

# Plot original data
    # plt.figure(figsize=(4,8))
    #
    # xx = [ row[0] for row in data ]
    # yy = [ row[1] for row in data ]
    # plt.plot(xx,yy,".",color="red")

# Plot edges of minimal spanning tree
#     X = np.array(data)
#     A = X[p1].T
#     B = X[p2].T
#
#     x_coords = np.vstack([A[0], B[0]])
#     y_coords = np.vstack([A[1], B[1]])

    # plt.plot(x_coords,y_coords,"-r",color="green")

# Plot potential arc centers - intersection points
#     xx = [ row[0] for row in int_points ]
#     yy = [ row[1] for row in int_points ]
#     plt.plot(xx,yy,".",color="blue")

# Plot arcs detected
#     for arc in arcs.values():
#         center = arc[0]
#         width,height = 2*arc[1],2*arc[1]
#         startAngle = arc[2]
#         endAngle = arc[3]
#         ax = plt.gca()
#         patch = Arc(center, width, height, startAngle, endAngle, edgecolor='green')
#         ax.add_patch(patch)
#
#     plt.axis("scaled")
#     plt.show()

    return arcs, filtered_data