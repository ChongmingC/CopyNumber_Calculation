# rDNA Copy Number Estimation Pipeline

A  pipeline to estimate rDNA copy number from BAM files using depth-based calculations.

## Project Structure

..../CopyNumber_Calculation
├── 1.1extract_merge_reads_test_data_paralle.sh
├── 1.2depth_bwa_5s_45s.sh
├── 1.3filter_0_16_parellel.sh
├── 1.4depth_calculation.sh
├── 2.1depth_results_exon_intron_blood_no_duplication.sh
├── 2.2batch_BRD_average_results_blood.sh
├── batch_BRD_average_results.py
├── calculate_CN_TCGA_py
│   ├── average_depth.py
│   ├── calculate_all_CN.py
│   ├── main.py
│   └── split_depth_files.py
├── intron_exon_no_duplication
│   ├── chr13_exon.bed
│   ├── chr13_intron.bed
│   ├── chr14_exon.bed
│   ├── chr14_intron.bed
│   ├── chr15_exon.bed
│   ├── chr15_intron.bed
│   ├── chr1_exon.bed
│   ├── chr1_intron.bed
│   ├── chr21_exon.bed
│   ├── chr21_intron.bed
│   ├── chr22_exon.bed
│   └── chr22_intron.bed
├── rdna_env.yml
└── rDNA_paper
    ├── 45S_U13369.1_Modified_16kb.fasta
    ├── 45S_U13369.1_Modified_16kb.fasta.amb
    ├── 45S_U13369.1_Modified_16kb.fasta.ann
    ├── 45S_U13369.1_Modified_16kb.fasta.bwt
    ├── 45S_U13369.1_Modified_16kb.fasta.pac
    ├── 45S_U13369.1_Modified_16kb.fasta.sa
    ├── 45S_U13369.1_Modified_forward_16kb.fasta
    ├── 45S_U13369.1_Modified_forward_16kb.fasta.amb
    ├── 45S_U13369.1_Modified_forward_16kb.fasta.ann
    ├── 45S_U13369.1_Modified_forward_16kb.fasta.bwt
    ├── 45S_U13369.1_Modified_forward_16kb.fasta.pac
    ├── 45S_U13369.1_Modified_forward_16kb.fasta.sa
    ├── 5S_X12811.1.fasta
    ├── 5S_X12811.1.fasta.amb
    ├── 5S_X12811.1.fasta.ann
    ├── 5S_X12811.1.fasta.bwt
    ├── 5S_X12811.1.fasta.pac
    ├── 5S_X12811.1.fasta.sa
    ├── complete_repeating_unit_U13369.1.fasta
    └── paper_rDNA.fasta


Current directory structure includes:
- rDNA_paper: folder containing reference rDNA sequences
- rdna_env.yml: file listing conda environment dependencies
- calculate_CN_TCGA_py: folder containing final copy number calculation scripts
- Four shell scripts for part 1:
  - 1.1extract_merge_reads_test_data_paralle.sh
  - 1.2depth_bwa_5s_45s.sh
  - 1.3filter_0_16_parellel.sh
  - 1.4depth_calculation.sh
- Two shell scripts and one Python script for part 2:
  - 2.1depth_results_exon_intron_blood_no_duplication.sh
  - 2.2batch_BRD_average_results_blood.sh
  - batch_BRD_average_results.py
-calculate_CN_TCGA_py: Calculate Copy Number


## Environment Setup

using rdna_env.yml

## Part 1 Compute Depth of rDNA

Run the following scripts one by one in this order:
1.1extract_merge_reads_test_data_paralle.sh
1.2depth_bwa_5s_45s.sh
1.3filter_0_16_parellel.sh
1.4depth_calculation.sh


Script 1.2depth_bwa_5s_45s.sh takes the most time, approximately 6 to 12 hours.
All other scripts take less than 60 minutes.

Before running, edit the shell scripts to set the following parameters:
Project_ID should be set to your Project_ID
input_dir should point to your BAM file directory

## Part 2 Compute Background Depth

Run the following scripts one by one in this order:
2.1depth_results_exon_intron_blood_no_duplication.sh
2.2batch_BRD_average_results_blood.sh

Script 2.2batch_BRD_average_results_blood.sh calls the Python script batch_BRD_average_results.py
The exon and intron ranges are provided in the folder named intron_exon_no_duplication

Script 2.1 takes about 16 to 40 hours to complete
Script 2.2 takes less than 1 hour to complete

Before running, edit the scripts to set:
Project_ID should be set to your Project_ID
input_dir should point to your BAM file directory

## Part 3 Calculate Copy Number

This part uses the results from Part 1 and Part 2 to compute the  copy number

Step 1 Create a root results directory:
Create a root dir like CN_results and inside it create a folder named with your Project_ID

Step 2 Copy the required files into the newly created folder:
Copy the folder $Project_ID/depth_results_blood
Copy the file BRD_Results/$Project_ID/blood_all_BRD.csv
Copy the file BRD_Results/$Project_ID/blood_chr13_14_15_21_22_exon_BRD.csv
Copy the file BRD_Results/$Project_ID/blood_chr1_exon_intron.csv

Step 3 Run the final Python script:
python calculate_CN_TCGA_py/main.py CN_results

The final result will be saved to
CN_results slash TCGA-BLCA_CN_all.csv

Example usage is provided in the comments of calculate_CN_TCGA_py/main.py
The runtime is approximately 1 to 10 minutes

## Note
Before running, edit the scripts to set:
#source /home/user/miniconda3/etc/profile.d/conda.sh
#conda activate rdna