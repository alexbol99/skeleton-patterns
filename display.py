import matplotlib.pyplot as plt
from matplotlib.patches import Arc

def plot(data, segments={}, arcs = {}):
    xx = [ row[0] for row in data ]
    yy = [ row[1] for row in data ]

    # Plot data
    plt.figure(figsize=(4,8))
    plt.plot(xx,yy,".",color="red")

    # Plot segments
    for seg in segments.values():
        plt.plot((seg[0],seg[2]),(seg[1],seg[3]),"-r",color="green")

    # Plot arcs
    for arc in arcs.values():
        center = arc[0]
        width,height = 2*arc[1],2*arc[1]
        startAngle = arc[2]
        endAngle = arc[3]
        ax = plt.gca()
        patch = Arc(center, width, height, startAngle, startAngle, edgecolor='green')
        ax.add_patch(patch)

    plt.axis("scaled")
    plt.show()
