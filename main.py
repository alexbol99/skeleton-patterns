# import matplotlib.pyplot as plt
# import time
from input import read_data
from segment_detector import detect_segments
from arc_detector import detect_arcs
from display import plot

data = read_data("medial.csv")
segments, filtered_data = detect_segments(data)
print(segments)
# plot(data, segments)

arcs, filtered_data = detect_arcs(filtered_data)
plot(data, segments, arcs)


# from lib_numpy.input import read_data
# from lib_numpy.segment_detector import detect_segments
# from lib_numpy.display import plot
#
#
# data = read_data("medial.csv")
#
# start = time.time()
# segments, filtered_data = detect_segments(data)
# end = time.time()
#
# print("Version numpy takes {} msec".format(end-start))
#
# print(segments)
# plot(data, segments)

