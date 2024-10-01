from line_segment import LineSegment, Point, Event
from bintrees import RBTree
import math
import sys

def sweep_line_alg(line_segments: list[LineSegment], query_point: Point):
    """
    The Sweepline algorithm implementation
    """
    status : RBTree[LineSegment] = RBTree()

    event_points: list[Event] = create_events(line_segments, query_point, status)
    event_points.sort()


    # Sweep line algorithm
    for event in event_points:
        if event.event_type == "start": 
            print("inserting")
            status.insert(key = event.segment, value = None)
        else: 
            print(f"Event removed: {event}")
            status.remove(event.segment)
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


def angle_between_lines(line1: LineSegment, line2: LineSegment):
    u_x = line1.p2.x - line1.p1.x
    u_y = line1.p2.y - line1.p1.y

    v_x = line2.p2.x - line2.p1.x
    v_y = line2.p2.y - line2.p1.y

    dot_prod = u_x * v_x + u_y * v_y
    cross_prod = u_x * v_y - u_y * v_x


    angle_rad = math.atan2(cross_prod, dot_prod)
    angle_deg = math.degrees(angle_rad) % 360  # Ensure angle is between 0 and 360 degrees
    return angle_deg



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


def create_events(line_segments: LineSegment, query_point: Point, status: RBTree) -> list[Event]:
    """
    Create the event points for the sweep line algorithm and initialise the status
    """
    event_points: list[Event] = []
    sweep_line = LineSegment(query_point, Point(sys.maxsize * -1, query_point.y))
    for line in line_segments:
        p1_angle = angle_between_lines(LineSegment(query_point, line.p1), sweep_line)
        p2_angle = angle_between_lines(LineSegment(query_point, line.p2), sweep_line)
        p1_dist = euclidian_distance(line.p1, query_point)
        p2_dist = euclidian_distance(line.p2, query_point)
        
        intersection_point = line_intersection(line.p1, line.p2, sweep_line.p1, sweep_line.p2)

        # Works because RBTree has duplicate protection
        if intersection_point is not None:
            intersection_distance = euclidian_distance(intersection_point, query_point)
            line.q_point_dist = intersection_distance
            status.insert(key = line, value = None)
            see_line_segment(status)

        if p1_angle == p2_angle:
            if p1_dist < p2_dist:
                event_points.append(Event(angle=p1_angle, dist=p1_dist, event_type="start", segment=line))
                event_points.append(Event(angle=p2_angle, dist=p2_dist, event_type="end", segment=line))
            else:
                event_points.append(Event(angle=p2_angle, dist=p2_dist, event_type="start", segment=line))
                event_points.append(Event(angle=p1_angle, dist=p1_dist, event_type="end", segment=line))
        else:
            if p1_angle < p2_angle:
                event_points.append(Event(angle=p1_angle, dist=p1_dist, event_type="start", segment=line))
                event_points.append(Event(angle=p2_angle, dist=p2_dist, event_type="end", segment=line))
            else:
                event_points.append(Event(angle=p2_angle, dist=p2_dist, event_type="start", segment=line))
                event_points.append(Event(angle=p1_angle, dist=p1_dist, event_type="end", segment=line))
        
    return event_points


