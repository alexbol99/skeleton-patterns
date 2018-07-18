from input import read_data
from segment_detector import detect_segments
from arc_detector import detect_arcs
from display import plot

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

file_path = filedialog.askopenfilename()

data = read_data(file_path)
segments, filtered_data = detect_segments(data)
# plot(filtered_data, segments)

arcs, filtered_data = detect_arcs(filtered_data)
plot(data, segments, arcs)
