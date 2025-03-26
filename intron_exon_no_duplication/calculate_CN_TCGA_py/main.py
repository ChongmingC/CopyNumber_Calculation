import average_depth
import calculate_all_CN
import split_depth_files
import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt
import sys

def main(Project_ID=None, root_dir=None):
    split_depth_files.split_depth_files(Project_ID, root_dir)
    average_depth.process_depth_files_for_all_rDNA(Project_ID, root_dir)
    calculate_all_CN.caculate_CN_for_all_rDNA(Project_ID, root_dir)

if __name__ == "__main__":
    # Check if command-line arguments are provided
    if len(sys.argv) > 2:
        Project_ID = sys.argv[1]
        root_dir = sys.argv[2]
        #no additional parsing needed since sys.argv passes the raw string as-is from the command line
        print(f"Project_ID: {Project_ID}")
        print(f"root_dir: {root_dir}")
        print(f"Whether path is exist: {os.path.exists(root_dir)}")
        main(Project_ID, root_dir)
    else:
        print("No arguments provided. Usage: python main.py <Project_ID> <root_dir>")  # error, no arguments provided

#     - Project_ID (str): The TCGA project ID.
#     - root_dir (str): The root directory where the project data is stored.
#  

#notice given Project_ID and root_dir, the main function will call the other functions to split depth files, calculate average depth and copy number for all rDNA regions
#and save the results to the specified directory

# Example usage:
#mkdir -p CN_results/TCGA-LUSC
#cp -r TCGA-LUSC/depth_results_blood CN_results/TCGA-LUSC
#cp BRD_Results/TCGA-LUSC/blood_all_BRD.csv BRD_Results/TCGA-LUSC/blood_chr13_14_15_21_22_exon_BRD.csv BRD_Results/TCGA-LUSC/blood_chr1_exon_intron.csv CN_results/TCGA-LUSC
#python calculate_CN_TCGA_py/main.py "TCGA-LUSC" "/home/Projects/CopyNumber_Calculation_test/CN_results"
