import os
import pandas as pd
import matplotlib.pyplot as plt




#notice 5S and 45s
def read_and_filter_depth(file_path, position_range=None):
    """
    Reads depth data from a file and filters it based on a position range.

    Parameters:
    - file_path (str): Path to the input file containing depth data.
    - position_range (tuple, optional): A tuple specifying the range of positions (min_position, max_position).

    Returns:
    - positions (list): List of filtered positions.
    - depths (list): List of filtered depths.
    """
    positions = []
    depths = []

    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            position = int(parts[1])
            depth = int(parts[2])

            # Apply position range filter if provided
            if position_range is None or (position_range[0] <= position <= position_range[1]):
                positions.append(position)
                depths.append(depth)

    return positions, depths


def calculate_average_depth(depths):
    """
    Calculates the average depth from a list of depths.

    Parameters:
    - depths (list): List of depth values.

    Returns:
    - float: Average depth.
    """
    return sum(depths) / len(depths) if depths else 0


def save_depth_distribution_plot(positions, depths, output_path, title='Depth Distribution along the Sequence'):
    """
    Saves a depth distribution plot as an image file.

    Parameters:
    - positions (list): List of positions.
    - depths (list): List of depth values.
    - output_path (str): Path to save the plot image.
    - title (str): Title of the plot.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(positions, depths, marker='o', linestyle='-', color='#377EB8', markersize=1)
    plt.title(title, fontsize=16)
    plt.xlabel('Position', fontsize=14)
    plt.ylabel('Depth', fontsize=14)
    plt.grid(True)
    plt.savefig(output_path)
    plt.close()


def process_depth_files(input_dir, output_dir="/depth/processed", rDNA_type="45S", Project_ID="Not", position_range=None, save_plots=False):
    """
    Processes multiple depth files in a directory, calculates average depth for a specified range, 
    and saves results in a summary table. Optionally, saves depth distribution plots.

    Parameters:
    - input_dir (str): Directory containing input files.
    - output_dir (str): Directory to save results and plots.
    - rDNA_type (str): Type of rDNA to process (e.g., '45S').
    - position_range (tuple, optional): Range of positions to filter depth data (min_position, max_position).
    - save_plots (bool): If True, saves depth distribution plots.
    """
    os.makedirs(output_dir, exist_ok=True)
    results = []
    print(output_dir)

    for filename in os.listdir(input_dir):
        filename_rDNA = filename.split("_")[2]
        if rDNA_type == filename_rDNA and filename.endswith('.txt'):
            file_path = os.path.join(input_dir, filename)
            base_name = filename.split('_')[0]  # Extract sample ID, e.g., 'TCGA-4Z-AA7Y-10A'

            # Read and filter data, then calculate average depth
            positions, depths = read_and_filter_depth(file_path, position_range)
            average_depth = calculate_average_depth(depths)

            # Save plot if requested
            if save_plots:
                plot_path = os.path.join(output_dir, f"{base_name}_depth_distribution.png")
                save_depth_distribution_plot(positions, depths, plot_path, title=f"{base_name} Depth Distribution")

            # Append results for summary table
            results.append({"Sample": f"{base_name}_{rDNA_type}", "Average Depth": average_depth})

    # Define summary file name with rDNA type and position range
    range_str = f"{position_range[0]}-{position_range[1]}" if position_range else "all"
    #summary_file_name = f"{rDNA_type}_{range_str}_{input_dir}_average_depth.csv"
    #summary_file_name = f"{rDNA_type}_{range_str}_average_depth.csv"
    summary_file_name = f"{rDNA_type}_{range_str}_{Project_ID}_average_depth.csv"
    summary_path = os.path.join(output_dir, summary_file_name)

    # Save results to a summary table
    summary_df = pd.DataFrame(results)
    summary_df.to_csv(summary_path, index=False)

    print(f"Processing complete. Summary saved to {summary_path}.")
    if save_plots:
        print("Depth distribution plots saved in", output_dir)

#example usage for process_depth_files
"""
#api blood 5S
#avoid duplicating, add tumor blood later
process_depth_files(
    input_dir="depth_results_blood_slicing_api", 
    output_dir="depth_average_csv", 
    rDNA_type="5S", 
    save_plots=False  #not save plots
)

#api blood 45S
process_depth_files(
    input_dir="depth_results_blood_slicing_api", 
    output_dir="depth_average_csv", 
    rDNA_type="45S", 
    save_plots=False  #not save plots
) """


def process_depth_files_for_all_rDNA(Project_ID=None, root_dir=None):
    """
    Processes depth files for all rDNA regions (45S, 18S, 5.8S, 28S) in the specified project directory.

    Parameters:
    - Project_ID (str): The TCGA project
    - root_dir (str): The root directory where the project data is stored.
    """
    if not Project_ID or not root_dir:
        raise ValueError("Project_ID and root_dir must be provided.")

    input_dir = os.path.join(root_dir, Project_ID, "depth_results_blood_5s_45s_18s_5.8s_28s")
    output_dir = os.path.join(root_dir, Project_ID, "average_depth_blood_csv")
    #print(input_dir)
    #print(output_dir)

    # Process depth files for each rDNA region
    for rDNA_type in ['5S', '45S', '18S', '5.8S', '28S']:
        process_depth_files(input_dir, output_dir, rDNA_type, Project_ID=Project_ID, save_plots=False)
        print(f"Processed average depth for {rDNA_type}.")

# Example usage
#process_depth_files_for_all_rDNA(Project_ID="TCGA-XXXX", root_dir="/home/user/projects")
#process_depth_files_for_all_rDNA(Project_ID="TCGA-XXXX", root_dir=".")
#process_depth_files_for_all_rDNA(Project_ID="TCGA-BLCA", root_dir="test1")