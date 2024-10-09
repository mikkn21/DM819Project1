import math
import string


class Point:
    def __init__(self, x : float, y : float):
        self.x = float(x)
        self.y = float(y) 

    def __str__(self):
        return f"{self.x} {self.y}"


def line_intersection(p1: Point, p2: Point, query_point: Point, extenstion_point: Point):
    """
    Find new intersections of the sweep line with the line segments
    """
    def det(a: Point, b: Point):
        return float(a.x * b.y - a.y * b.x)
    
    epsilon = 1e-9
    xdiff = Point(p1.x - p2.x, query_point.x - extenstion_point.x)
    ydiff = Point(p1.y - p2.y, query_point.y - extenstion_point.y)

    div = det(xdiff, ydiff)
    if abs(div) < epsilon:  # Lines are parallel or coincident
        # Check for collinearity
        if abs(det(Point(query_point.x - p1.x, query_point.y - p1.y), Point(extenstion_point.x - p1.x, extenstion_point.y - p1.y))) < epsilon:
            
            def overlap_1d(a1, a2, b1, b2):
                """
                check if two 1D intervals overlap
                used in the collinear case
                """
                return max(min(a1, a2), min(b1, b2)) <= min(max(a1, a2), max(b1, b2)) + epsilon

            if overlap_1d(p1.x, p2.x, query_point.x, extenstion_point.x) and overlap_1d(p1.y, p2.y, query_point.y, extenstion_point.y):
                if euclidian_distance(p1, query_point) < euclidian_distance(p2, query_point):
                    return p1
                else:
                    return p2
        return None  


    d = Point(det(p1, p2), det(query_point, extenstion_point))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div


    def is_between(a:float, b:float , c:float , epsilon:float):
        return min(a, b) - epsilon <= c <= max(a, b) + epsilon

    if (is_between(p1.x, p2.x, x, epsilon) and is_between(p1.y, p2.y, y, epsilon) and
        is_between(query_point.x, extenstion_point.x, x, epsilon) and is_between(query_point.y, extenstion_point.y, y, epsilon)):
        return Point(x, y)
    else:
        return None
    
def euclidian_distance(p1: Point, p2: Point):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)


def normalize_vector(dx:float, dy:float):
    magnitude = math.sqrt(dx ** 2 + dy ** 2)
    return float(dx / magnitude), float(dy / magnitude)

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
        if isinstance(other, LineSegment):
            direction_vector_x = self.event_point.x - self.query_point.x
            direction_vector_y = self.event_point.y - self.query_point.y


            norm_direction_x, norm_direction_y = normalize_vector(direction_vector_x, direction_vector_y)

            farthest_distance = max(
                euclidian_distance(self.query_point, self.p1),
                euclidian_distance(self.query_point, self.p2),
                euclidian_distance(self.query_point, other.p1),
                euclidian_distance(self.query_point, other.p2)
            )

            extension_point = Point(
                self.query_point.x + norm_direction_x * farthest_distance * 2,  # Extend twice as far as the farthest point
                self.query_point.y + norm_direction_y * farthest_distance * 2
            )
            
            self_intersection_point = line_intersection(self.p1, self.p2, self.query_point, extension_point)
            other_intersection_point = line_intersection(other.p1, other.p2, self.query_point, extension_point)
            if self_intersection_point is None:
                return False
            elif other_intersection_point is None:
                return True
            elif self_intersection_point is None and other_intersection_point is None:
                raise ValueError("Both intersection points are None")
            else: 
                return euclidian_distance(self_intersection_point, self.query_point) < euclidian_distance(other_intersection_point, self.query_point)
        return False
    
    def __gt__(self, other):
        if isinstance(other, LineSegment):
            direction_vector_x = self.event_point.x - self.query_point.x
            direction_vector_y = self.event_point.y - self.query_point.y


            norm_direction_x, norm_direction_y = normalize_vector(direction_vector_x, direction_vector_y)

            farthest_distance = max(
                euclidian_distance(self.query_point, self.p1),
                euclidian_distance(self.query_point, self.p2),
                euclidian_distance(self.query_point, other.p1),
                euclidian_distance(self.query_point, other.p2)
            )

            extension_point = Point(
                self.query_point.x + norm_direction_x * farthest_distance * 2,  # Extend twice as far as the farthest point
                self.query_point.y + norm_direction_y * farthest_distance * 2
            )
            
            self_intersection_point = line_intersection(self.p1, self.p2, self.query_point, extension_point)
            other_intersection_point = line_intersection(other.p1, other.p2, self.query_point, extension_point)
            if self_intersection_point is None:
                return False
            elif other_intersection_point is None:
                return True
            elif self_intersection_point is None and other_intersection_point is None:
                raise ValueError("Both intersection points are None")
            else: 
                return euclidian_distance(self_intersection_point, self.query_point) > euclidian_distance(other_intersection_point, self.query_point)
        return False


    def __eq__(self, other):
        if isinstance(other, LineSegment):
            return (math.isclose(self.p1.x, other.p1.x) and
                    math.isclose(self.p1.y, other.p1.y) and
                    math.isclose(self.p2.x, other.p2.x) and
                    math.isclose(self.p2.y, other.p2.y))
        return False
    

    def __str__(self):
        return f"{self.p1} {self.p2}"
    
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
                        return self.dist > other.dist
        return False
    
    def __str__(self) -> str:
        return f"{self.segment}, {self.event_type}, {self.angle}"

