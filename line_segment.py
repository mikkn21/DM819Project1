import string

class Point:
    def __init__(self, x : float, y : float):
        self.x = float(x)
        self.y = float(y) 
        self.line_segment = None
        self.angle_to_q : float = None

    def __eq__(self, other):
        if isinstance(other, Point):
            return (self.x == other.x and self.y == other.y)
        return False

    def __str__(self):
        return f"({self.x}, {self.y})"
    

class LineSegment:
    def __init__(self, p1 : Point, p2 : Point ):
        self.p1: Point = p1
        self.p2: Point = p2
        self.seen: bool = False
        self.q_point_dist: float = None
     
    # Define the less-than operator for comparing LineSegment objects
    def __lt__(self, other):
        if isinstance(other, LineSegment):
            return self.q_point_dist < other.q_point_dist
        return False
    
    def __gt__(self, other):
        if isinstance(other, LineSegment):
            return self.q_point_dist > other.q_point_dist
        return False

    def __eq__(self, other):
        if isinstance(other, LineSegment):
            return (self.p1.x == other.p1.x and self.p1.y == other.p1.y and
                    self.p2.x == other.p2.x and self.p2.y == other.p2.y)
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

    






