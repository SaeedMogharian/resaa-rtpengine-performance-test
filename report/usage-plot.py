import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Function to read and process a pidstat log file for total CPU usage
def process_pidstat_total_cpu(file_path, threshold=10.0):
    # Read the file
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Initialize lists for storing the extracted data
    total_cpu_data = []

    # Extract relevant data from each line
    for line in lines:
        if line.startswith("Average:"):
            continue  # skip the average lines
        columns = line.split()
        if len(columns) > 6:
            try:
                total_cpu = float(columns[5])  # Extract %CPU (total usage)
                total_cpu_data.append(total_cpu)
            except:
                continue

    # Create a DataFrame with the extracted data
    df = pd.DataFrame({'total_cpu': total_cpu_data})

    # Find the first index where CPU usage increases significantly
    start_index = df[df['total_cpu'] > threshold].first_valid_index()

    # Return the DataFrame sliced from the detected start index
    if start_index is not None:
        df = df.loc[start_index:].reset_index(drop=True)

    return df


# Function to plot and save total CPU usage comparison
def plot_total_cpu_comparison(dataset, names):
    plt.figure(figsize=(10, 6))

    n = len(dataset)
    # Use a built-in color map (e.g., 'tab10' has 10 distinct colors)
    colors = plt.cm.tab10.colors
    # Plot total CPU usage for each log file
    for i in range(n):
        y = [val + i for val in range(n)]
        dt = dataset[i]
        plt.plot(dt.index, dt['total_cpu'], label=f'Log {os.path.basename(names[i]).split('.')[0]}', color=colors[i % len(colors)])

    # Formatting the plot
    plt.xlabel('Log Entry (Step)')
    plt.ylabel('Total CPU Usage (%)')
    plt.title('Comparison of total CPU usage across log entries (aligned by CPU spike)')
    plt.legend()
    plt.grid(True)

    # Save the plot as a PNG file
    plt.tight_layout()
    output_path = '-'.join([os.path.splitext(os.path.basename(path))[0] for path in names]) + '.png'
    plt.savefig(output_path, format='png')
    print(f"Plot saved as {output_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("input log file")
        sys.exit(1)

    log_files = sys.argv[1:]
    # log_files = ['.\\t2500\\t2500.log', '.\\t2500\\t2600.log' ,'.\\t2500\\t2700.log' ]

    # print(log_files)

    dfl = []
    for d in log_files:
        df_total_cpu = process_pidstat_total_cpu(d, threshold=10.0)
        dfl.append(df_total_cpu)

    # Save the plot instead of showing it
    plot_total_cpu_comparison(dfl, names=log_files)
