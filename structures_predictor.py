import os
import subprocess
import time

# Define the folder containing the FASTA files and other required paths
fasta_folder = './all_fasta'
template_path = './templates'
output_folder = './all_structures'
os.makedirs(output_folder, exist_ok=True)

# Loop through all files in the 'all_fasta' folder
for filename in os.listdir(fasta_folder):
    if filename.endswith('.fasta'):
        fasta_file_path = os.path.join(fasta_folder, filename)
        
        output_folder_for_file = os.path.join(output_folder, filename.replace('_processed.fasta', ''))

        pdb_files_exist = (
            os.path.exists(output_folder_for_file) and
            any(f.endswith('.pdb') for f in os.listdir(output_folder_for_file))
        )

        command = [
            'sbatch', './YOUR_RUN_SCRIPT_OF_COLABFOLD.job',
            '-i', fasta_file_path,
            '-o', output_folder_for_file,
            '--', '--templates',
            '--custom-template-path', template_path,
            '--amber',
            '--use-gpu-relax',
        ]
        
        # if jobs fail
        if not pdb_files_exist:
            try:
                print(f"Submitting job for {filename}...")
                subprocess.run(command, check=True, capture_output=True, text=True)
                print(f"Job submitted for {filename}.")
                time.sleep(0.5)
            except subprocess.CalledProcessError as e:
                print(f"Error occurred while processing {filename}: {e.stderr}")
        else:
            print(f"Skipping {filename} — PDB files already exist.")