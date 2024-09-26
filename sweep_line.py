from line_segment import LineSegment, Point, Event
from bintrees import RBTree
import math
import sys

def sweep_line_alg(line_segments: list[LineSegment], query_point: Point):
    """
    The Sweepline algorithm implementation
    """
    status = RBTree()

    event_points: list[Event] = create_events(line_segments, query_point)
    event_points.sort(key=lambda event: (event.angle, event.event_type != "start", event.dist if event.event_type == "start" else -event.dist))
    
    for event in event_points:
        print(event)
    
        #sys.exit() 

    # for event in event_points:
    #     print(event)

    # Initialise status with the segments that intersect the sweepline from the start.
    # sweep_end_point: Point = Point(x = (sys.maxsize * -1), y = query_point.y)
    # for line in line_segments:
    #     intersection_point = line_intersection(line.p1, line.p2, query_point, sweep_end_point)
    #     if intersection_point in event_points:
    #         event_points.remove(intersection_point)
    #     if intersection_point is not None:
    #         intersection_distance = euclidian_distance(intersection_point, query_point)
    #         line.q_point_dist = intersection_distance
    #         status.insert(key = line, value = intersection_distance)
    # see_line_segment(status)



    # Sweep line algorithm
    for event in event_points:
        if event.event_type == "start":
            event.segment.q_point_dist = event.dist
            status.insert(event.segment, event.segment.q_point_dist)
        else: 
            status.remove(event.segment)
        """if event.line_segment.q_point_dist is not None and status.__contains__(point.line_segment):
            status.remove(point.line_segment)
        else:
            for line in status:
                # s_l_i_p = sweep line intersectoin point
                s_l_i_p = line_intersection(line.p1, line.p2, query_point, point)
                if s_l_i_p is not None:
                    line.q_point_dist = euclidian_distance(s_l_i_p, query_point)
                            
            point.line_segment.q_point_dist = euclidian_distance(point, query_point)
            status.insert(key = point.line_segment, value = point.line_segment.q_point_dist)  """
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



def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]


def angle_between_lines(line1: LineSegment, line2: LineSegment):
    # Direction vector of line1
    u_x = line1.p2.x - line1.p1.x
    u_y = line1.p2.y - line1.p1.y
    # Direction vector of line2
    v_x = line2.p2.x - line2.p1.x
    v_y = line2.p2.y - line2.p1.y

    # Compute the dot product and cross product of the direction vectors
    dot_prod = u_x * v_x + u_y * v_y
    cross_prod = u_x * v_y - u_y * v_x

    # Calculate the angle in radians between the two vectors
    angle_rad = math.atan2(cross_prod, dot_prod)
    # Convert the angle from radians to degrees
    angle_deg = math.degrees(angle_rad) % 360  # Ensure angle is between 0 and 360 degrees

    return angle_deg





def create_events(line_segments: LineSegment, query_point: Point) -> list[Event]:
    event_points: list[Event] = []
    sweep_line = LineSegment(query_point, Point(sys.maxsize * -1, query_point.y))
    for line in line_segments:
        p1_angle = angle_between_lines(LineSegment(query_point, line.p1), sweep_line)
        p2_angle = angle_between_lines(LineSegment(query_point, line.p2), sweep_line)
        p1_dist = euclidian_distance(line.p1, query_point)
        p2_dist = euclidian_distance(line.p2, query_point)
        # p2_angle = calculate_angle(query_point, line.p2)
        # p1_dist = euclidian_distance(query_point, line.p1)
        # p2_dist = euclidian_distance(query_point, line.p2)

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