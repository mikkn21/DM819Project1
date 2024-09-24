from line_segment import LineSegment, Point
from bintrees import RBTree
import math


def sweep_line_alg(line_segments: list[LineSegment], query_point: Point):
    """
    The Sweepline algorithm implementation
    """
    status = RBTree()

    event_points: list[Point] = []
    
    for line in line_segments:
        p1_angle = calculate_angle(line.p1, query_point)
        line.p1.angle_to_q = p1_angle
        event_points.append(line.p1)

        p2_angle = calculate_angle(line.p2, query_point)
        line.p2.angle_to_q = p2_angle
        event_points.append(line.p2)

    # Events points ordered by angle from query point 
    event_points.sort(key = lambda x: x.angle_to_q) # RETURN HERE LATER FOR DISTANCE


    for point in event_points:
        if point.line_segment.q_point_dist is not None and status.__contains__(point.line_segment):
            status.remove(point.line_segment)
        else:
            for line in status:
                # s_l_i_p = sweep line intersectoin point
                s_l_i_p = line_intersection(line.p1, line.p2, query_point, point)
                if s_l_i_p is not None:
                    line.q_point_dist = euclidian_distance(s_l_i_p, query_point)
                            
            point.line_segment.q_point_dist = euclidian_distance(point, query_point)
            status.insert(key = point.line_segment, value = point.line_segment.q_point_dist)  
        
        see_line_segment(status)



    return [line for line in line_segments if line.seen]
             

def euclidian_distance(p1: Point, p2: Point):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def see_line_segment(status: RBTree):
    """
    Report the line segment as seen
    """
    if not status.is_empty():
        min_key = status.min_key()
        if not min_key.seen:
            min_key.seen = True


def calculate_angle(p1 : Point, p2 : Point):
    """
    Find the angle between two points for sorting the event points
    """
    delta_x = p2.x - p1.x
    delta_y = p2.y - p1.y

    angle_radians = math.atan2(delta_y, delta_x)
    angle_degrees = math.degrees(angle_radians)

    if angle_degrees < 0:
        angle_degrees += 360

    return angle_degrees



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