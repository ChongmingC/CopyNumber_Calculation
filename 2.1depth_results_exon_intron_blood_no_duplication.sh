#!/bin/bash

#SBATCH --account=CancerEvolution
#SBATCH --time=48:00:00
#SBATCH --mem=32g
#SBATCH --cpus-per-task=128

#load conda
source /home/user/miniconda3/etc/profile.d/conda.sh
conda activate rdna

# Set the number of threads
THREADS=64
THREADS_PER_TASK=2

# Define directories for BED files, BAM files, and output root directory
#Project_ID="TCGA-PAAD"
Project_ID="TCGA-BLCA" 
BAM_DIR="/home/user/CancerEvolution/Datasets/TCGA_WGS/data/$Project_ID"
BED_DIR="intron_exon_no_duplication"
OUTPUT_ROOT_DIR="$Project_ID/depth_results_exon_intron_blood_no_duplication"

# Create output root directory if it doesn't exist
mkdir -p "$OUTPUT_ROOT_DIR"

# Initialize job counter to control the number of concurrent tasks
job_count=0

# Process BAM files with BED regions
for BAM_FILE in "$BAM_DIR"/*.bam; do
    # Extract base filename
    BAM_BASENAME=$(basename "$BAM_FILE" .bam)

    # Create per-BAM output directory
    BAM_OUTPUT_DIR="${OUTPUT_ROOT_DIR}/${BAM_BASENAME}"
    mkdir -p "$BAM_OUTPUT_DIR"

    #  Process each BED file
    for BED_FILE in "$BED_DIR"/*.bed; do
        # Get BED filename without extension
        BED_BASENAME=$(basename "$BED_FILE" .bed)

        # Define output path
        OUTPUT_FILE="${BAM_OUTPUT_DIR}/${BAM_BASENAME}_${BED_BASENAME}_depth.txt"

        # Launch depth calculation
        (
            echo "Processing ${BAM_BASENAME} with ${BED_BASENAME}"
            samtools depth -@ $THREADS_PER_TASK -a -b "$BED_FILE" "$BAM_FILE" > "$OUTPUT_FILE"
            echo "Depth calculation completed for ${BAM_BASENAME} with ${BED_BASENAME}"
        ) &

        # Job control for parallel processing
        job_count=$((job_count + 1))

        if [[ $job_count -ge $THREADS ]]; then
            wait  
            job_count=0  
        fi
    done
done

# Final wait to ensure all background tasks are complete before ending the script
wait

echo "888All BAM file depth calculations are complete. Results saved in ${OUTPUT_ROOT_DIR}"