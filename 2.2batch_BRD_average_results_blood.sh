#!/bin/bash

#SBATCH --account=CancerEvolution
#SBATCH --time=4:00:00
#SBATCH --mem=32g
#SBATCH --cpus-per-task=4

#load conda
source /home/user/miniconda3/etc/profile.d/conda.sh
conda activate rdna

# Set the number of threads
THREADS=4

#Project_ID="TCGA-PAAD"
Project_ID="TCGA-BLCA"
BRD_Results="BRD_Results/$Project_ID"
# Create output BRD_Results directory if it doesn't exist
mkdir -p "$BRD_Results"

###############################
# 1.1 blood-->process_all_files
root_dir_blood="$Project_ID/depth_results_exon_intron_blood_no_duplication"
output_file_blood_all="$BRD_Results/blood_all_BRD.csv"
label="blood"

python -c "from batch_BRD_average_results import process_all_files; \
process_all_files(root_dir='$root_dir_blood', output_file='$output_file_blood_all', label='$label')" &

###############################
# 1.2 blood_chr13_14_15_21_22_exon/45S-->  process_multiple_files_with_label
output_file_blood_45S_BRD="$BRD_Results/blood_chr13_14_15_21_22_exon_BRD.csv"
python -c "from batch_BRD_average_results import process_multiple_files_with_label; \
process_multiple_files_with_label(root_dir='$root_dir_blood', output_file='$output_file_blood_45S_BRD', label='$label', \
selected_files=['chr13_exon_depth','chr14_exon_depth','chr15_exon_depth','chr21_exon_depth','chr22_exon_depth'], custom_label='chr13_14_15_21_22_exon')" &

###############################
# 1.3. blood-5S/chr1_exon_intron:--> process_multiple_files_with_label
output_file_blood_5S_BRD="$BRD_Results/blood_chr1_exon_intron.csv"
python -c "from batch_BRD_average_results import process_multiple_files_with_label; \
process_multiple_files_with_label(root_dir='$root_dir_blood', output_file='$output_file_blood_5S_BRD', label='$label', \
selected_files=['chr1_intron_depth','chr1_exon_depth'], custom_label='chr1_exon_intron')" &

wait

