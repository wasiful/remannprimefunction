import csv
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D # Import for 3D plotting

def is_prime(num):
    """
    Checks if a number is prime.
    A simple primality test function.
    """
    if num < 2:
        return False
    # Iterate from 2 to the square root of the number
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True

def find_primes_and_calculate_values(start_n, end_n):
    """
    Finds primes between (n-1)^2 and n^2 for a range of n,
    calculates x and y, and prepares data for CSV and plotting.
    
    Args:
        start_n (int): The starting value for n.
        end_n (int): The ending value for n.

    Returns:
        tuple: A tuple containing the data for the CSV and the points for the plot.
    """
    csv_data = [['n', 'p', 'x = n^2 - p', 'y = p - (n-1)^2', 'x/y']]
    plot_points = []

    print("Processing values for n...")
    for n in range(start_n, end_n + 1):
        # Define the lower and upper bounds for the prime search
        lower_bound = (n - 1) ** 2
        upper_bound = n ** 2
        
        print(f"n = {n}: searching for primes between {lower_bound} and {upper_bound}")

        # Find all prime numbers within the specified range
        for p in range(lower_bound + 1, upper_bound):
            if is_prime(p):
                # Calculate x and y based on the corrected formulas
                x = upper_bound - p
                y = p - lower_bound
                
                # Calculate the ratio and round it to 5 decimal places
                xy_ratio = round(x / y, 5) if y != 0 else 0

                # Append the calculated values to our data lists
                csv_data.append([n, p, x, y, xy_ratio])
                # Append x, y, and the prime p for 3D plotting
                plot_points.append((x, y, p))
                print(f"  - Found prime p={p}. Calculated (x,y) = ({x},{y})")

    return csv_data, plot_points

def write_to_csv(filename, data):
    """
    Writes the provided data to a CSV file.
    
    Args:
        filename (str): The name of the CSV file to create.
        data (list): A list of lists representing the rows to write.
    """
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(data)
        print(f"\nSuccessfully saved data to {filename}")
    except IOError as e:
        print(f"Error writing to file {filename}: {e}")

def plot_graph(points):
    """
    Creates and displays a 3D scatter plot for the given x, y, z points.
    
    Args:
        points (list): A list of (x, y, z) tuples, where z is the prime number.
    """
    if not points:
        print("No points to plot.")
        return

    # Unzip the list of tuples into separate lists for x, y, and z coordinates
    x_vals, y_vals, z_vals = zip(*points)

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Create the 3D scatter plot, coloring points by their z-value (the prime number)
    scatter = ax.scatter(x_vals, y_vals, z_vals, c=z_vals, cmap='viridis', alpha=0.7)
    
    # Set titles and labels for the axes
    ax.set_title('3D Graph of x, y, and Prime Number (p)\n(for n from 5 to 15)', fontsize=16)
    ax.set_xlabel('x = n^2 - p', fontsize=12)
    ax.set_ylabel('y = p - (n-1)^2', fontsize=12)
    ax.set_zlabel('Prime Number (p)', fontsize=12)
    
    # Add a color bar to show the mapping of colors to prime numbers
    fig.colorbar(scatter, ax=ax, label='Prime Number (p)')
    
    print("Displaying 3D plot...")
    plt.show()


if __name__ == '__main__':
    # Define the range for n
    N_START = 5
    N_END = 100
    CSV_FILENAME = 'prime_data.csv'

    # Run the main logic
    prime_data, points_for_plot = find_primes_and_calculate_values(N_START, N_END)
    
    # Write the data to a CSV file
    write_to_csv(CSV_FILENAME, prime_data)
    
    # Generate and display the plot
    plot_graph(points_for_plot)

