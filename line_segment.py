class Point:
    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __str__(self):
        return f"({self.x}, {self.y})"


class LineSegment:
    def __init__(self, p1, p2 ):
        self.p1 = p1
        self.p2 = p2
    

    def __str__(self):
        return f"{self.p1}, {self.p2}"

    def get_coordinates(self):
        """Returns the coordinates of the endpoints as a tuple (x1 y1 x2 y2)."""
        return (self.p1.x, self.p1.y, self.p2.x, self.p2.y)
    






