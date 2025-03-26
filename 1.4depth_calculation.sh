#!/bin/bash

#SBATCH --account=CancerEvolution
#SBATCH --time=3:00:00
#SBATCH --mem=32g
#SBATCH --cpus-per-task=32

# Load conda
source /home/user/miniconda3/etc/profile.d/conda.sh
conda activate rdna

#step5 depth
# Set the number of threads
#THREADS=16
MAX_JOBS=30
CURRENT_JOBS=0

# Define input and output directories
Project_ID="TCGA-BLCA" #321
input_dir="$Project_ID/filtered_bwa_results"
output_dir="$Project_ID/sorted_bam_index_filtered_bwa_results"
depth_dir="$Project_ID/depth_results_blood"

# Create output directories if they do not exist
mkdir -p "$output_dir" "$depth_dir"

# Iterate through all .sam files in the input directory
for sam_file in "$input_dir"/*.sam; do
    base_name=$(basename "$sam_file" .sam)

    bam_file="$output_dir/${base_name}.bam"
    sorted_bam_file="$output_dir/${base_name}.sorted.bam"
    depth_file="$depth_dir/${base_name}_depth.txt"

    {
        echo "Processing $sam_file"

        # Check if SAM file exists and is not empty
        if [ ! -s "$sam_file" ]; then
            echo "Error: SAM file $sam_file is empty or missing, skipping..."
            exit 1
        fi

        # Convert SAM to BAM
        echo "Converting $sam_file to BAM format..."
        samtools view -h -Sb "$sam_file" > "$bam_file"

        # Validate BAM file creation
        if [ ! -s "$bam_file" ]; then
            echo "Error: BAM file $bam_file is empty, samtools view failed!"
            exit 1
        fi

        # Sort BAM
        echo "Sorting BAM file $bam_file..."
        samtools sort "$bam_file" -o "$sorted_bam_file"

        # check sorted BAM 
        if [ ! -s "$sorted_bam_file" ]; then
            echo "Error: Sorted BAM file $sorted_bam_file is empty, samtools sort failed!"
            exit 1
        fi

        # Index sorted BAM file
        echo "Indexing sorted BAM file $sorted_bam_file..."
        samtools index "$sorted_bam_file"

        # Depth Calculation
        echo "Calculating depth for $sorted_bam_file..."
        samtools depth -a "$sorted_bam_file" > "$depth_file"

        echo "Processed $sam_file -> $sorted_bam_file with depth output in $depth_file"
    } &

    ((CURRENT_JOBS++))
    if [ "$CURRENT_JOBS" -eq "$MAX_JOBS" ]; then
        wait
        CURRENT_JOBS=0
    fi
done

# Final wait for remaining jobs
wait
echo "All jobs completed successfully!"
