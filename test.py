import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file into a DataFrame
csv_file_path = 'line_sweep_completely_disjoint_test_data.csv'  # Replace with your file path
df = pd.read_csv(csv_file_path)

# Plotting each line segment
plt.figure(figsize=(8, 8))

for _, row in df.iterrows():
    x_values = [row['x1'], row['x2']]
    y_values = [row['y1'], row['y2']]
    plt.plot(x_values, y_values, marker='o')

# Adding labels and title
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Line Segments from CSV')
plt.grid(True)

# Show the plot
plt.show()
