import os
import pandas as pd

def calculate_copy_number(Project_ID=None, average_depth_file=None, BRD_file=None, output_file=None):
    """
    Calculates copy number based on average depth and BRD depth.

    Parameters:
    - average_depth_file (str): Path to the average depth file.
    - BRD_file (str): Path to the BRD file.

    Returns:
    - pd.DataFrame: DataFrame with calculated copy numbers.
    """
    # Read average depth and BRD files
    average_depth = pd.read_csv(average_depth_file)
    average_depth["Sample_ID"] = average_depth["Sample"].str.split("_").str[0]
    average_depth["chr"] = average_depth["Sample"].str.split("_").str[1]
    average_depth.drop(columns=["Sample"], inplace=True)
    average_depth = average_depth[["Sample_ID", "chr", "Average Depth"]]

    BRD = pd.read_csv(BRD_file)
    BRD["BRD.Average_Depth"] = BRD["Average_Depth"]
    BRD.drop(columns=["Average_Depth"], inplace=True)

    # Merge dataframes
    merged = pd.merge(average_depth, BRD, on="Sample_ID", how="inner")

    # Calculate copy number
    merged["copy_number"] = merged["Average Depth"] / merged["BRD.Average_Depth"]
    #print(merged)

    #only keep necessary columns
    merged = merged[["Sample_ID", "copy_number", "Depth_File", "chr", "Label"]]
    merged["Project_ID"] = Project_ID

    #print unmatched samples if any
    unmatched = average_depth[~average_depth["Sample_ID"].isin(merged["Sample_ID"])]
    if not unmatched.empty:
        print("Samples not matched:")
        print(unmatched)
    
    # Save results to a file if specified
    if output_file:
        merged.to_csv(output_file, index=False)
        print(f"Copy number results saved to {output_file}")

#example usage
"""
average_depth_file = "test1/TCGA-BLCA/average_depth_blood_csv/45S_all_TCGA-BLCA_average_depth.csv"
BRD_file = "test1/TCGA-BLCA/blood_chr13_14_15_21_22_exon_BRD.csv"
output_file = "test1/TCGA-BLCA_45S_copy_number_results.csv"
calculate_copy_number(average_depth_file, BRD_file, output_file)
"""

def caculate_CN_for_all_rDNA(Project_ID=None, root_dir=None):
    """
    Calculates copy number for all rDNA regions (45S, 18S, 5.8S, 28S) in the specified project directory.

    Parameters:
    - Project_ID (str): The TCGA project
    - root_dir (str): The root directory where the project data is stored.
    """
    if not Project_ID or not root_dir:
        raise ValueError("Project_ID and root_dir must be provided.")
    
    average_depth_dir = os.path.join(root_dir, Project_ID, "average_depth_blood_csv")
    BRD_5S = os.path.join(root_dir, Project_ID, f"blood_chr1_exon_intron.csv")
    BRD_45S = os.path.join(root_dir, Project_ID, f"blood_chr13_14_15_21_22_exon_BRD.csv")
    output_path = os.path.join(root_dir, Project_ID,"copy_number_results")
    os.makedirs(output_path, exist_ok=True)
    output_summary = os.path.join(root_dir, f"{Project_ID}_CN_all.csv")

    for files in os.listdir(average_depth_dir):
        if files.endswith(".csv"):
            rDNA_type = files.split("_")[0]
            if rDNA_type == "5S":
                average_depth_file = os.path.join(average_depth_dir, files)
                output_file = os.path.join(output_path, f"{Project_ID}_{rDNA_type}_CN_results.csv")
                calculate_copy_number(Project_ID=Project_ID, average_depth_file=average_depth_file, BRD_file=BRD_5S, output_file=output_file)
                print(f"Calculated copy number for {rDNA_type}.")
            if rDNA_type in ['45S', '18S', '5.8S', '28S']: #?
                average_depth_file = os.path.join(average_depth_dir, files)
                output_file = os.path.join(output_path, f"{Project_ID}_{rDNA_type}_CN_results.csv")
                calculate_copy_number(Project_ID=Project_ID, average_depth_file=average_depth_file, BRD_file=BRD_45S, output_file=output_file)
                print(f"Calculated copy number for {rDNA_type}.")
    
    #merge all copy number results in outputsummary
    all_results = []
    for files in os.listdir(output_path):
        if files.endswith(".csv"):
            file_path = os.path.join(output_path, files)
            df = pd.read_csv(file_path)
            all_results.append(df)
    summary_df = pd.concat(all_results)
    summary_df.to_csv(output_summary, index=False)

    print(f"Copy number results saved to {output_summary}")
    