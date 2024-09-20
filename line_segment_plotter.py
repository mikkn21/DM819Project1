import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt  # Import after setting the backend


class LineSegmentPlotter:
    def __init__(self, line_segments):
        self.line_segments = line_segments

    def plot(self):
        plt.figure(figsize=(8, 8))

        # Extract all x and y coordinates
        x_coords = []
        y_coords = []

        for segment in self.line_segments:
            plt.plot([segment.x1, segment.x2], [segment.y1, segment.y2], marker='o')
            x_coords.extend([segment.x1, segment.x2])
            y_coords.extend([segment.y1, segment.y2])

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