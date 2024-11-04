# main.py

import subprocess
import sys
import os

# Add the parent directory of 'ml_pipeline' to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Set environment variables
# Set environment variables for R paths directly in PATH
os.environ["PATH"] += r";C:\Users\jeram\miniconda3\envs\myenv_py38\Lib\R\bin"
os.environ["PATH"] += r";C:\Users\jeram\miniconda3\envs\myenv_py38\Lib\R\bin\x64"
os.environ["PATH"] += r";C:\Users\jeram\miniconda3\envs\myenv_py38\Lib\R\lib"
os.environ["PATH"] += r";C:\Users\jeram\miniconda3\envs\myenv_py38\Lib\R\library"
os.environ["R_HOME"] = r"C:\Users\jeram\miniconda3\envs\myenv_py38\Lib\R"
os.environ["R_LIBS_USER"] = r"C:\Users\jeram\miniconda3\envs\myenv_py38\Lib\R\library"
# Not used on Windows
# os.environ["LD_LIBRARY_PATH"] = r"C:\Users\jeram\miniconda3\envs\myenv_py38\Lib\R\lib"

# Disable R's bytecode compilation for this session
os.environ["R_COMPILE_PKGS"] = "0"

'''
# Verify paths
print("PATH:", os.environ["PATH"])
print("R_HOME:", os.environ["R_HOME"])
print("LD_LIBRARY_PATH:", os.environ.get("LD_LIBRARY_PATH"))
'''

# Import rpy2 after setting paths
import rpy2.robjects as robjects

# Suppress gettext warnings in the R environment
robjects.r('options(warn=-1)')  # Disable all warnings
robjects.r('suppressPackageStartupMessages(library(gettext))')  # Suppress gettext messages
robjects.r('message("DESeq2 Analysis setup complete without gettext warnings.")')

from rna_seq_pipeline.deseq2_pipeline import run_deseq2
from ml_pipeline.process_deseq2_results import filter_significant_genes, save_filtered_results_to_csv
from data_fetching import fetch_expression_data, fetch_sample_info

def main():
    # Fetch expression data and sample metadata
    expression_data = fetch_expression_data()
    sample_info = fetch_sample_info()

    # Run DESeq2 Analysis
    deseq2_results = run_deseq2(expression_data, sample_info)

    # Filter significant results for ML
    significant_genes = filter_significant_genes(deseq2_results)
    save_filtered_results_to_csv(significant_genes, 'data/significant_genes.csv')


if __name__ == "__main__":
    main()
