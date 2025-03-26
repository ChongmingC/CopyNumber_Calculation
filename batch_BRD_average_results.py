import os
import csv

def calculate_file_average(file_path):
    """Calculate the average depth and number of lines in a single file"""
    total_depth = 0
    total_length = 0

    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) != 3:
                continue
            try:
                depth = int(parts[2])  # 提取深度值
                total_depth += depth
                total_length += 1
            except ValueError:
                continue

    if total_length == 0:
        return 0, 0  # Avoid dividing by zero
    return round(total_depth / total_length,3), total_length

    

def process_all_files(root_dir, output_file, label):
    """Function 1: Process all files and calculate the average depth of each file"""
    results = []

    for sample_id in os.listdir(root_dir):  # Iterate through all sample folders
        sample_dir = os.path.join(root_dir, sample_id)
        if not os.path.isdir(sample_dir):
            continue

        for file_name in os.listdir(sample_dir):  # Iterate through all samples
            file_path = os.path.join(sample_dir, file_name)
            if not os.path.isfile(file_path):
                continue

            # get the basename
            core_name = file_name.replace(f"{sample_id}_", "").replace(".txt", "")

            avg_depth, length = calculate_file_average(file_path)
            results.append({
                "Sample_ID": sample_id,
                "Depth_File": core_name,
                "Average_Depth": avg_depth,
                "Length": length,
                "Label": label
            })

    # save
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ["Sample_ID", "Depth_File", "Average_Depth", "Length", "Label"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Function 1 The result has been saved to: {output_file}")

#no use
def process_selected_files(root_dir, output_file, label, selected_files):
    """Function 2: Processes only the specified files and calculates their average depth."""
    results = []

    for sample_id in os.listdir(root_dir):  
        sample_dir = os.path.join(root_dir, sample_id)
        if not os.path.isdir(sample_dir):
            continue

        for file_name in os.listdir(sample_dir):  
            file_path = os.path.join(sample_dir, file_name)
            if not os.path.isfile(file_path):
                continue

            
            core_name = file_name.replace(f"{sample_id}_", "").replace(".txt", "")

            
            if core_name not in selected_files:
                continue

            avg_depth, length = calculate_file_average(file_path)
            results.append({
                "Sample_ID": sample_id,
                "Depth_File": core_name,
                "Average_Depth": avg_depth,
                "Length": length,
                "Label": label
            })

    
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ["Sample_ID", "Depth_File", "Average_Depth", "Length", "Label"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"Function 2 The result has been saved to: {output_file}")


def process_multiple_files_with_label(root_dir, output_file, label, selected_files, custom_label):
    """Function 3: Processes a specified number of files and calculates the average depth of the merge, retaining the result to 3 decimal places."""
    results = []

    for sample_id in os.listdir(root_dir):  
        sample_dir = os.path.join(root_dir, sample_id)
        if not os.path.isdir(sample_dir):
            continue

        # Store the results of all target files in the current sample
        sample_results = []

        for file_name in os.listdir(sample_dir):  
            file_path = os.path.join(sample_dir, file_name)
            if not os.path.isfile(file_path):
                continue

            # basename
            core_name = file_name.replace(f"{sample_id}_", "").replace(".txt", "")

            # Check if the file is in the specified list
            if core_name not in selected_files:
                continue

            avg_depth, length = calculate_file_average(file_path)
            sample_results.append({
                "Average_Depth": avg_depth,
                "Length": length
            })

        # Merge to calculate the total average depth and total length of the current sample
        total_length = sum(r["Length"] for r in sample_results)
        if total_length > 0:
            total_avg_depth = sum(r["Average_Depth"] * r["Length"] for r in sample_results) / total_length
        else:
            total_avg_depth = 0

        results.append({
            "Sample_ID": sample_id,
            "Depth_File": custom_label,
            "Average_Depth": total_avg_depth,
            "Length": total_length,
            "Label": label
        })

    # save
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ["Sample_ID", "Depth_File", "Average_Depth", "Length", "Label"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in results:
            # Retain 3 decimal places
            row["Average_Depth"] = round(row["Average_Depth"], 3)
            writer.writerow(row)

    print(f"Function 3 Results have been saved to. {output_file}")
    

'''
if __name__ == "__main__":
    #blood all_files blood
    process_all_files(
        root_dir="depth_results_exon_intron_blood_no_duplication",
        output_file="blood_all_BRD.csv",
        label="blood"
    )
    
    #tumor all_files
    process_all_files(
        root_dir="depth_results_exon_intron_tumor_no_duplication",
        output_file="tumor_all_BRD.csv",
        label="tumor"
    )

    #blood chr13_14_15_21_22_exon
    process_multiple_files_with_label(
        root_dir="depth_results_exon_intron_blood_no_duplication",
        output_file="blood_chr13_14_15_21_22_exon_BRD.csv",
        label="blood",
        selected_files=["chr13_exon_depth", "chr14_exon_depth", "chr15_exon_depth", "chr21_exon_depth", "chr22_exon_depth"],
        custom_label="chr13_14_15_21_22_exon"
    )
    
    #tumor chr13_14_15_21_22_exon
    process_multiple_files_with_label(
        root_dir="depth_results_exon_intron_tumor_no_duplication",
        output_file="tumor_chr13_14_15_21_22_exon_BRD.csv",
        label="tumor",
        selected_files=["chr13_exon_depth", "chr14_exon_depth", "chr15_exon_depth", "chr21_exon_depth", "chr22_exon_depth"],
        custom_label="chr13_14_15_21_22_exon"
    )

    #blood chr1_exon_intron
    process_multiple_files_with_label(
        root_dir="depth_results_exon_intron_blood_no_duplication",
        output_file="blood_chr1_exon_intron.csv",
        label="blood",
        selected_files=["chr1_intron_depth", "chr1_exon_depth"],
        custom_label="chr1_exon_intron"
    )
    
    #tumor chr1_exon_intron
    process_multiple_files_with_label(
        root_dir="depth_results_exon_intron_tumor_no_duplication",
        output_file="tumor_chr1_exon_intron.csv",
        label="tumor",
        selected_files=["chr1_intron_depth", "chr1_exon_depth"],
        custom_label="chr1_exon_intron"
    )
'''


