import math
import string


class Point:
    def __init__(self, x : float, y : float):
        self.x = float(x)
        self.y = float(y) 

    def __str__(self):
        return f"({self.x}, {self.y})"

# event_point: Point # the current event point the sweep line is intersecting
# query_point_global: Point # query point

def line_intersection(p1: Point, p2: Point, p3: Point, p4: Point):
    """
    Find new intersections of the sweep line with the line segments
    """
    def det(a: Point, b: Point):
        return a.x * b.y - a.y * b.x
    
    xdiff = Point(p1.x - p2.x, p3.x - p4.x)
    ydiff = Point(p1.y - p2.y, p3.y - p4.y)

    div = det(xdiff, ydiff)
    if div == 0:
        return None  # Lines do not intersect

    d = Point(det(p1, p2), det(p3, p4))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div

    def is_between(a, b, c):
        return min(a, b) <= c <= max(a, b)

    if (is_between(p1.x, p2.x, x) and is_between(p1.y, p2.y, y) and
        is_between(p3.x, p4.x, x) and is_between(p3.y, p4.y, y)):
        return Point(x, y)
    else:
        return None
    
def euclidian_distance(p1: Point, p2: Point):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

class LineSegment:
    def __init__(self, p1 : Point, p2 : Point):
        self.p1: Point = p1
        self.p2: Point = p2
        self.seen: bool = False
        self.event_point: Point = None 
        self.query_point: Point = None
    
    def set_event_point(self, event_point : Point):
        self.event_point = event_point

    def __lt__(self, other):
        #print(f"self: {self}, other: {other}")
        if isinstance(other, LineSegment):
            # print(f"query point: {self.query_point}, event point: {self.event_point}")
            
            direction_vector_x = self.event_point.x - self.query_point.x
            direction_vector_y = self.event_point.y - self.query_point.y

            extend_factor = max(
                euclidian_distance(self.query_point, self.p1),
                euclidian_distance(self.query_point, self.p2),
                euclidian_distance(self.query_point, other.p1),
                euclidian_distance(self.query_point, other.p2))
            
            extention_point = Point(
                self.query_point.x + direction_vector_x * extend_factor, 
                self.query_point.y + direction_vector_y * extend_factor)
            print(f"query point: {self.query_point}")
            print(f"event point: {self.event_point}")
            print(f"extention point: {extention_point}")

            self_intersection_point: Point = line_intersection(self.p1, self.p2, self.query_point, extention_point)
            other_intersection_point: Point = line_intersection(other.p1, other.p2, self.query_point, extention_point)
            return euclidian_distance(self_intersection_point, self.query_point) < euclidian_distance(other_intersection_point, self.query_point)
        return False


    def __eq__(self, other):
        if isinstance(other, LineSegment):
            # print("i am in equal")
            return (math.isclose(self.p1.x, other.p1.x) and
                    math.isclose(self.p1.y, other.p1.y) and
                    math.isclose(self.p2.x, other.p2.x) and
                    math.isclose(self.p2.y, other.p2.y))
        return False


    def __str__(self):
        return f"{self.p1}, {self.p2}"
    
    def get_coordinates(self):
        """Returns the coordinates of the endpoints as a tuple (x1 y1 x2 y2)."""
        return (self.p1.x, self.p1.y, self.p2.x, self.p2.y)

class Event:
    def __init__(self, angle: float, dist: float, event_type: string, segment: LineSegment):
        self.angle = angle
        self.dist = dist
        self.event_type = event_type # not string?
        self.segment = segment
    
    def __lt__(self, other):
        if isinstance(other, Event):    
            if not self.angle == other.angle:
                return self.angle < other.angle
            else:
                if not self.event_type == other.event_type:
                    return self.event_type == "start"
                else:
                    if self.event_type == "start":
                        return self.dist < other.dist
                    else:
                        return self.dist > other.dis
        return False
    
    def __str__(self) -> str:
        return f"{self.segment}, {self.event_type}, {self.angle}"

