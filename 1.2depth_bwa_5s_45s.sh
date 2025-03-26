#!/bin/bash

#SBATCH --account=CancerEvolution
#SBATCH --time=30:00:00
#SBATCH --mem=64g
#SBATCH --cpus-per-task=32

#load conda
source /home/user/miniconda3/etc/profile.d/conda.sh
conda activate rdna

# Set the number of threads
THREADS=$SLURM_CPUS_PER_TASK 


#step 1.2  Perform BWA MEM alignment -> results will be stored in SAM files
# output and input paths
Project_ID="TCGA-BLCA" 
fastq_dir="$Project_ID/wgs_fastq_GL000220v1_1q42_10_v1"
output_dir="$Project_ID/bwa_results"
reference_5S="rDNA_paper/5S_X12811.1.fasta"
reference_45S="rDNA_paper/45S_U13369.1_Modified_forward_16kb.fasta"

# Create the output directory if it does not exist
mkdir -p "$output_dir"

# Iterate over all FASTQ file
for fastq_file in "$fastq_dir"/*.fastq; do
    # Extract the base filename, e.g., TCGA-4Z-AA7S-10A_1q42 or TCGA-4Z-AA7S-10A_GL000220v1
    base_name=$(basename "$fastq_file" .fastq)

    # Determine which reference sequence to use based on the filename
    if [[ "$base_name" == *"1q42"* ]]; then
        # Align to 5S_X12811.1.fasta
        output_file="${output_dir}/${base_name}_5S.sam"
        echo "Aligning $fastq_file to 5S reference..."
        bwa mem -t "$THREADS" "$reference_5S" "$fastq_file" > "$output_file"

    elif [[ "$base_name" == *"GL000220v1"* ]]; then
        #  45S_U13369.1_Modified_forward_16kb.fasta
        output_file="${output_dir}/${base_name}_45S.sam"
        echo "Aligning $fastq_file to 45S..."
        bwa mem -t "$THREADS" "$reference_45S" "$fastq_file" > "$output_file"
    else
        echo "Skipping $fastq_file: does not match expected naming conventions."
    fi
done

echo "All FASTQ files have been processed."