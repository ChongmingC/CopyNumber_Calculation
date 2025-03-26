#!/bin/bash

#SBATCH --account=CancerEvolution
#SBATCH --time=6:00:00
#SBATCH --mem=8g
#SBATCH --cpus-per-task=16

#load conda
source /home/user/miniconda3/etc/profile.d/conda.sh
conda activate rdna

#step1.3 remain aligned reads
# Set the number of threads
THREADS=15

# output and input paths
Project_ID="TCGA-BLCA" 
input_dir="$Project_ID/bwa_results"
output_dir="$Project_ID/filtered_bwa_results"

# create
mkdir -p "$output_dir"

# count the number of processes currently running
count=0

# Iterate through all .sam files 
for sam_file in "$input_dir"/*.sam; do
    # base name
    base_name=$(basename "$sam_file" .sam)
    
    # output files
    output_file="$output_dir/${base_name}_f0_16.sam"

    # using awk to filter
    echo "Processing $sam_file -> $output_file"
    awk '($1 ~ /^@/) || ($2 == 0 || $2 == 16)' "$sam_file" > "$output_file" &

    # Count and control the number of parallel tasks
    ((count++))
    
    # When the maximum number of parallel tasks is reached, wait for all tasks to complete
    if [[ $count -eq $THREADS ]]; then
        wait
        count=0
    fi
  
done

# wait
wait

echo "All files processed."



