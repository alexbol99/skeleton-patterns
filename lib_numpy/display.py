import matplotlib.pyplot as plt
'''
    Plot data as numpy arrays
'''
def plot(data, segments=[]):

    plt.figure(figsize=(4,8))
    plt.plot(data[:,0],data[:,1],".",color="red")
    for seg in segments.values():
        plt.plot((seg[0],seg[2]),(seg[1],seg[3]),"-r",color="green")
    plt.axis("scaled")
    plt.show()
