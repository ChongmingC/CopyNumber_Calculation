import os
import shutil



def split_depth_files(Project_ID=None, root_dir=None, input_dir=None, output_dir=None, relabel_positions=True):
    """
    Processes 45S depth files in the specified input directory, splitting data into separate files
    for 18S, 5.8S, and 28S regions, with optional renumbering of positions from 1.

    Parameters:
    - Project_ID (str, optional): The TCGA project
    - root_dir (str, optional): The root directory where the project data is stored.
    - input_dir (str, optional): Path to the directory containing input depth files.
    - output_dir (str, optional): Path to the directory where the output files will be saved.
    If Project_ID and root_dir are provided, input_dir and output_dir are generated automatically.
    - relabel_positions (bool): If True, re-labels position coordinates from 1 for each rRNA region.
    
    Output files:
    For each 45S file, creates three output files:
    - '<sample_id>_18S_depth.txt' for the 18S rRNA region.
    - '<sample_id>_5.8S_depth.txt' for the 5.8S rRNA region.
    - '<sample_id>_28S_depth.txt' for the 28S rRNA region.
    """
    # Automatically generate input_dir and output_dir if Project_ID and root_dir are provided
    if Project_ID and root_dir:
        input_dir = os.path.join(root_dir, Project_ID, "depth_results_blood")
        output_dir = os.path.join(root_dir, Project_ID, "depth_results_blood_5s_45s_18s_5.8s_28s")
    elif not input_dir or not output_dir:
        raise ValueError("Either (Project_ID and root_dir) or (input_dir and output_dir) must be provided.")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    print(f"Processing depth files from: {input_dir}")
    print(f"Saving processed files to: {output_dir}")

    # Copy all files from input_dir to output_dir
    for file_name in os.listdir(input_dir):
        source_path = os.path.join(input_dir, file_name)
        dest_path = os.path.join(output_dir, file_name)

        # Only process files, ignore subdirectorie
        if os.path.isfile(source_path):
            shutil.copy2(source_path, dest_path)
            #print(f"Moved: {source_path} → {dest_path}")

    print(f"All 45s 5s depth results files have been moved to {output_dir}.")
    
    # Define the ranges for each rRNA region
    ranges = {
        '18S': (3657, 5527),
        '5.8S': (6623, 6779),
        '28S': (7935, 12969)
    }

    # Ensure the output directory exists
    #os.makedirs(output_dir, exist_ok=True)

    # List all files in the input directory and filter for 45S files
    for filename in os.listdir(input_dir):
        if '45S' in filename and filename.endswith('.txt'):  # Only process files with '45S' in the name and .txt extension
            input_file = os.path.join(input_dir, filename)
            base_name = filename.split('_')[0]  # Extract sample ID, e.g., 'TCGA-4Z-AA7Y-10A'
            
            # Generate output file paths
            output_files = {
                '18S': os.path.join(output_dir, f"{base_name}_GL000220v1_18S_depth.txt"),
                '5.8S': os.path.join(output_dir, f"{base_name}_GL000220v1_5.8S_depth.txt"),
                '28S': os.path.join(output_dir, f"{base_name}_GL000220v1_28S_depth.txt")
            }

            # Open output files for writing
            with open(output_files['18S'], 'w') as file_18S, \
                 open(output_files['5.8S'], 'w') as file_5_8S, \
                 open(output_files['28S'], 'w') as file_28S:
                
                # Read and process the input file line by line
                try:
                    with open(input_file, 'r') as file:
                        for line in file:
                            parts = line.strip().split('\t')
                            try:
                                position = int(parts[1])
                                depth = parts[2]  # Assuming depth is in the third column
                            except (ValueError, IndexError):
                                print(f"Skipping invalid line: {line.strip()}")
                                continue

                            # Write to the appropriate file based on the position range
                            if ranges['18S'][0] <= position <= ranges['18S'][1]:
                                new_position = position - ranges['18S'][0] + 1 if relabel_positions else position
                                file_18S.write(f"{parts[0]}\t{new_position}\t{depth}\n")
                            elif ranges['5.8S'][0] <= position <= ranges['5.8S'][1]:
                                new_position = position - ranges['5.8S'][0] + 1 if relabel_positions else position
                                file_5_8S.write(f"{parts[0]}\t{new_position}\t{depth}\n")
                            elif ranges['28S'][0] <= position <= ranges['28S'][1]:
                                new_position = position - ranges['28S'][0] + 1 if relabel_positions else position
                                file_28S.write(f"{parts[0]}\t{new_position}\t{depth}\n")

                except FileNotFoundError:
                    print(f"File {input_file} not found.")
                except IOError:
                    print(f"Error reading file {input_file}.")

            print(f"Data for {filename} has been split into separate files in {output_dir} for 18S, 5.8S, and 28S regions.")

# Example usage
# split_files("/data/depth_files", "/depth/18s_5.8s_28s", relabel_positions=True)
#split_depth_files(Project_ID="TCGA-XXXX", root_dir="/home/user/projects", relabel_positions=True)
#split_depth_files(Project_ID="TCGA-XXXX", root_dir=".", relabel_positions=True) # Use current directory
