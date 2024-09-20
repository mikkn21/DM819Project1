import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt  # Import after setting the backend


class LineSegmentPlotter:
    def __init__(self, line_segments, query_point):
        self.line_segments = line_segments
        self.query_point = query_point

    def plot(self):
        plt.figure(figsize=(8, 8))

        # Extract all x and y coordinates
        x_coords = []
        y_coords = []

        for segment in self.line_segments:
            x1, y1, x2, y2 = segment.get_coordinates()
            
            # Plot the line segment
            plt.plot([x1, x2], [y1, y2], marker='o')
            
            # Collect coordinates for limits
            x_coords.extend([x1, x2])
            y_coords.extend([y1, y2])


        # Include the query point in the coordinates
        if self.query_point:
            x_coords.append(self.query_point.x)
            y_coords.append(self.query_point.y)

            # Plot the query point
            plt.plot(self.query_point.x, self.query_point.y, 'ro')  # Red dot
            plt.text(self.query_point.x, self.query_point.y, ' p', color='red', fontsize=12, verticalalignment='bottom', horizontalalignment='left')

        # Calculate the limits based on the coordinates
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)

        # Add some padding to the limits for better visibility
        padding = 1
        plt.xlim(x_min - padding, x_max + padding)
        plt.ylim(y_min - padding, y_max + padding)
        
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('2D Line Segments')
        plt.grid()
        plt.axhline(0, color='black', linewidth=0.5, ls='--')
        plt.axvline(0, color='black', linewidth=0.5, ls='--')

        # Save the figure as a PDF
        plt.savefig("result.pdf", format='pdf')
        plt.close()