import re
import sys 
from line_segment import Point, LineSegment
from line_segment_plotter import LineSegmentPlotter
from sweep_line import sweep_line_alg, line_intersection

# Regular expression pattern to match numbers, handling various separators
coordinate_pattern = re.compile(r"[-+]?\d*\.?\d+")

input_file = None

if len(sys.argv) > 2:
    print("Error: Too many arguments.")
    exit()
elif len(sys.argv) == 2:
    input_file = sys.argv[1]
else:
    input_file = input("File name: ")

line_segments: LineSegment = []
query_point: Point = None

with open(input_file, "r") as file:
    line_number = 0
    query_point_count = 0
    for line in file:
        line_number = line_number + 1


        coordinates = coordinate_pattern.findall(line)
        if len(coordinates) == 0:
            continue # Skip empty lines:
        if len(coordinates) == 4:
            x1, y1, x2, y2 = coordinates
            p1: Point = Point(x1, y1)
            p2: Point = Point(x2, y2)
            line_segment = LineSegment(p1, p2)
            p1.line_segment = line_segment
            p2.line_segment = line_segment
            line_segments.append(line_segment)
        elif len(coordinates) == 2: 
            if query_point_count == 1:
                print(f"Error: More than one query point found on line {line_number}: '{line.strip()}'.")
                print("Only one query point is allowed in the data file.")
                sys.exit(1)
            x, y = coordinates
            query_point = Point(x, y)
            query_point_count += 1  
        else:
            print(f"Warning: Incorrect format on line {line_number}: '{line.strip()}'.")
            print("Expected format: 'x1 y1 x2 y2 \\n' or 'x y \\n' ")
            print("where x and y are numbers seperate by any delimiter.")
            sys.exit(1) 


if query_point is None:  
    print("Error: Query point not found in data file.")
    print("Expected format: 'x y \\n' ")
    sys.exit(1)   



## Call line sweep alg here 
visible_line_segments = sweep_line_alg(line_segments, query_point)

## print result
for line_segment in visible_line_segments:
    print(line_segment)


## plot on graph 
plotter = LineSegmentPlotter(line_segments, query_point, visible_line_segments)
plotter.plot()





