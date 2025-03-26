#!/bin/bash

#SBATCH --account=CancerEvolution
#SBATCH --time=6:00:00
#SBATCH --mem=16g
#SBATCH --cpus-per-task=32

#load conda
source /home/user/miniconda3/etc/profile.d/conda.sh
conda activate rdna


#step1.1: extract 1q42 + GL000220v1 --> sam
# Set the number of threads
#THREADS=16
max_jobs=32



# Define input and output directories
Project_ID="TCGA-BLCA" 
input_dir="/home/user/CancerEvolution/Datasets/TCGA_WGS/data/$Project_ID"
output_sam_dir="$Project_ID/wgs_sam_GL000220v1_1q42_10_v1"
output_fastq_dir="$Project_ID/wgs_fastq_GL000220v1_1q42_10_v1"
tmp_log_dir="$output_fastq_dir/tmp_logs"
final_log="$output_fastq_dir/$(basename "$0" .sh).log"

# Create the output directory if it does not exist
mkdir -p "$output_sam_dir"
mkdir -p "$output_fastq_dir"
mkdir -p "$tmp_log_dir"

#remove tmp logs
: > "$final_log"
declare -a tmp_logs=()


# Iterate over all BAM files in the input directory
for input_bam in "$input_dir"/*.bam; do
    # basename, like TCGA-4Z-AA7S-10A
    base_name=$(basename "$input_bam" .bam)

    sorted_bam="${input_dir}/${base_name}_sorted.bam"
    bai_file="${sorted_bam}.bai" 

    # output name
    output_gl000220="${base_name}_GL000220v1.sam"
    output_chr1="${base_name}_1q42.sam"
    output_fastq_gl000220="${base_name}_GL000220v1.fastq"
    output_fastq_chr1="${base_name}_1q42.fastq"

    # tmp logs
    curr_log="${tmp_log_dir}/${base_name}.log"
    tmp_logs+=("$curr_log")

    echo "Submitting job for $base_name..."

    #index
    {
        echo "Processing $base_name..."
      
        #  scaffold chrUn_GL000220v1 --> SAM files
        samtools view -h "$input_bam" chrUn_GL000220v1 > "$output_sam_dir/$output_gl000220"

        # chr1:226743523-231781906 --> SAM files
        samtools view -h "$input_bam" chr1:226743523-231781906 > "$output_sam_dir/$output_chr1"

        # scaffold chrUn_GL000220v1 --> FASTQ 
        samtools fastq "$output_sam_dir/$output_gl000220" > "$output_fastq_dir/$output_fastq_gl000220"

        # chr1:226743523-231781906--> FASTQ 
        samtools fastq "$output_sam_dir/$output_chr1" > "$output_fastq_dir/$output_fastq_chr1"

        echo "===FASTQ completed for $base_name ===="   
    } &> "$curr_log" &

    # If the number of background tasks reaches the upper limit, wait for any one task to complete
    while (( $(jobs -p | wc -l) >= max_jobs )); do
        wait -n
    done
    
done
wait

# tmp logs to final log
echo "================= all tasks logs =================" >> "$final_log"
for logfile in "${tmp_logs[@]}"; do
    echo -e "\n--------- ${logfile} ---------" >> "$final_log"
    cat "$logfile" >> "$final_log"
done

echo "All file processing is complete. Logs are saved in: $final_log"