import matplotlib.pyplot as plt

from input import read_data
from segment_detector import detect_segments

data = read_data("medial.txt")
segments, filtered_data = detect_segments(data)
print(segments)

xx = [ row[0] for row in filtered_data ]
yy = [ row[1] for row in filtered_data ]

plt.figure(figsize=(4,8))
plt.plot(xx,yy,".",color="red")
for seg in segments.values():
    plt.plot((seg[0],seg[2]),(seg[1],seg[3]),"-r",color="green")
plt.axis("scaled")
plt.show()






