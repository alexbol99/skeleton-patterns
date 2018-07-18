# import matplotlib as mpl
# mpl.use('TkAgg')
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

def plot(data, segments={}, arcs = {}):
    xx = [ row[0] for row in data ]
    yy = [ row[1] for row in data ]

    # Plot data
    plt.figure(1, figsize=(4,8))
    plt.plot(xx,yy,".",color="red")
    plt.axis("scaled")

    plt.figure(2, figsize=(4, 8))
    # Plot segments
    for seg in segments:
        plt.plot((seg[0],seg[2]),(seg[1],seg[3]),"-r",color="green")

    # Plot arcs
    for arc in arcs:                     # .values():
        center = arc[0]
        width,height = 2*arc[1],2*arc[1]
        startAngle = math.degrees(arc[2])
        endAngle = math.degrees(arc[3])
        ax = plt.gca()
        patch = Arc(center, width, height, 0, startAngle, endAngle, edgecolor='green')
        ax.add_patch(patch)

    # import math
    # patch = Arc((44750,40000), 200, 200, 0, 57, 37, edgecolor='orange')
    # ax.add_patch(patch)

    plt.axis("scaled")
    plt.show()
