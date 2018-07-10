# import matplotlib.pyplot as plt
# import time
from lib.input import read_data
from lib.segment_detector import detect_segments
from lib.display import plot

data = read_data("medial.txt")
segments, filtered_data = detect_segments(data)
print(segments)
plot(data, segments)



# from lib_numpy.input import read_data
# from lib_numpy.segment_detector import detect_segments
# from lib_numpy.display import plot
#
#
# data = read_data("medial.txt")
#
# start = time.time()
# segments, filtered_data = detect_segments(data)
# end = time.time()
#
# print("Version numpy takes {} msec".format(end-start))
#
# print(segments)
# plot(data, segments)

