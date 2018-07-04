import matplotlib.pyplot as plt

from input import read_data
from segment_detection import detect_segments

data = read_data("medial.txt")
segments = detect_segments(data)
print(segments)

xx = [ row[0] for row in data ]
yy = [ row[1] for row in data ]

plt.figure(figsize=(4,8))
plt.plot(xx,yy,"-r")
for seg in segments:
    plt.plot((seg[0],seg[2]),(seg[1],seg[3]),"-r",color="green")
plt.axis("scaled")
plt.show()

