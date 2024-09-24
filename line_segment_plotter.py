import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt 


class LineSegmentPlotter:
    def __init__(self, line_segments, query_point, visible_line_segments):
        self.line_segments = line_segments
        self.query_point = query_point
        self.visible_line_segments = visible_line_segments

    def plot(self):
        """
        Plots the line segments and the query point.
        
        """
        plt.figure(figsize=(8, 8))

        # Extract all x and y coordinates
        x_coords = []
        y_coords = []


        # Handle query point         
        x_coords.append(self.query_point.x)
        y_coords.append(self.query_point.y)

        # Plot the query point
        plt.plot(self.query_point.x, self.query_point.y, marker='o', color='blue')  
        plt.text(self.query_point.x, self.query_point.y, ' p', color='blue', fontsize=12, verticalalignment='bottom', horizontalalignment='left')


        # Handle line segments
        for segment in self.line_segments:
            x1, y1, x2, y2 = segment.get_coordinates()
            
            # Plot the line segment
            plt.plot([x1, x2], [y1, y2], marker='o', color='red')
            
            x_coords.extend([x1, x2])
            y_coords.extend([y1, y2])


        # Calculate the limits based on the coordinates
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)


        # Handle visible line segments
        for segment in self.visible_line_segments:
            x1, y1, x2, y2 = segment.get_coordinates()
            
            # Plot the line segment
            plt.plot([x1, x2], [y1, y2], marker='o', color='green')
            
        

        # Add some padding to the limits for better visibility
        padding = 1
        plt.xlim(x_min - padding, x_max + padding)
        plt.ylim(y_min - padding, y_max + padding)
        
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.title('Result')
        plt.grid()
        plt.axhline(0, color='black', linewidth=0.5, ls='--')
        plt.axvline(0, color='black', linewidth=0.5, ls='--')

        # Save the figure as a PDF
        plt.savefig("result.pdf", format='pdf')
        plt.close()