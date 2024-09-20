import re
from line_segment import LineSegment
from line_segment_plotter import LineSegmentPlotter 

# Regular expression pattern to match numbers, handling various separators
coordinate_pattern = re.compile(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?")

input_file = input("File name: ")
line_segments = []

with open(input_file, "r") as file:
    for line in file:
        coordinates = coordinate_pattern.findall(line)
        if len(coordinates) == 4:
            x1, y1, x2, y2 = coordinates
            line_segments.append(LineSegment(x1, y1, x2, y2))




plotter = LineSegmentPlotter(line_segments)
plotter.plot()





