from line_segment import LineSegment, Point, Event, line_intersection, euclidian_distance
from bintrees import RBTree
import math
import sys

def sweep_line_alg(line_segments: list[LineSegment], query_point: Point):
    """
    The Sweepline algorithm implementation
    """
    status : RBTree[LineSegment] = RBTree()

    init_line_segments: list[LineSegment] = []
    event_points: list[Event] = create_events(line_segments, query_point, status, init_line_segments)
    event_points.sort()
    for line in init_line_segments:
        line.set_event_point(event_points[0])
        status.insert(key = line, value = None)

    for thing in status:
        print(f"thing: {thing}")
    if status.is_empty():
                print("Empty")
    print(" ")

    # Sweep line algorithm
    for event in event_points:
        print(f"Current event: {event} - {event.event_type}")
        if event.event_type == "start": 
            #print("inserting")
            event.segment.set_event_point(event.segment.p1)
            #print(f"event point: {event.segment.event_point}")
            status.insert(key = event.segment, value = None)
            print(f"event insert: {event.segment}")
            for thing in status:
                print(f"tree: {thing}")
            if status.is_empty():
                print("Empty")
            print(" ")
        else: 
            #print(f"Event removed: {event}")
            event.segment.set_event_point(event.segment.p1)
            status.remove(event.segment)
            print(f"event remove: {event.segment}")
            for thing in status:
                print(f"tree: {thing}")
            if status.is_empty():
                print("Empty")
            print(" ")
        see_line_segment(status)
    return [line for line in line_segments if line.seen]
             

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


def create_events(line_segments: LineSegment, query_point: Point, status: RBTree, init_lines: list[LineSegment]) -> list[Event]:
    """
    Create the event points for the sweep line algorithm and initialise the status
    """
    event_points: list[Event] = []
    sweep_line = LineSegment(query_point, Point(sys.maxsize * -1, query_point.y))
    for line in line_segments:
        print(f"Handling line: {line}")
        line.query_point = query_point
        p1_angle = angle_between_lines(LineSegment(query_point, line.p1), sweep_line)
        p2_angle = angle_between_lines(LineSegment(query_point, line.p2), sweep_line)
        p1_dist = euclidian_distance(line.p1, query_point)
        p2_dist = euclidian_distance(line.p2, query_point)
        
        intersection_point = line_intersection(line.p1, line.p2, sweep_line.p1, sweep_line.p2)

        # Works because RBTree has duplicate protection
        if intersection_point is not None:
            intersection_distance = euclidian_distance(intersection_point, query_point)
            line.q_point_dist = intersection_distance
            #status.insert(key = line, value = None)
            init_lines.append(line)
            #see_line_segment(status)
            if p1_angle == p2_angle:
                if p1_dist < p2_dist:
                    event_points.append(Event(angle=p1_angle, dist=p1_dist, event_type="end", segment=line))
                    event_points.append(Event(angle=p2_angle, dist=p2_dist, event_type="start", segment=line))
                else:
                    event_points.append(Event(angle=p2_angle, dist=p2_dist, event_type="end", segment=line))
                    event_points.append(Event(angle=p1_angle, dist=p1_dist, event_type="start", segment=line))
            else:
                if p1_angle < p2_angle:
                    event_points.append(Event(angle=p1_angle, dist=p1_dist, event_type="end", segment=line))
                    event_points.append(Event(angle=p2_angle, dist=p2_dist, event_type="start", segment=line))
                else:
                    event_points.append(Event(angle=p2_angle, dist=p2_dist, event_type="end", segment=line))
                    event_points.append(Event(angle=p1_angle, dist=p1_dist, event_type="start", segment=line))
        
        else:    
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


