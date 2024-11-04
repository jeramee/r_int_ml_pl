# tests/test_process_deseq2_results.py

import sys
import os
import pytest
import pandas as pd
from pymongo import MongoClient

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

try:
    import rpy2.robjects as ro
    ro.r('source("gettext_override.R")')
except Exception as e:
    print(f"R initialization error: {e}")

# Mock DESeq2 results for testing
sample_deseq2_results = pd.DataFrame({
    "gene": ["Gene1", "Gene2", "Gene3", "Gene4", "Gene5"],
    "log2FoldChange": [1.5, -2.3, 0.8, 1.1, -1.8],
    "padj": [0.01, 0.03, 0.2, 0.05, 0.02]
})

from ml_pipeline.process_deseq2_results import filter_significant_genes, save_filtered_results

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["rna_seq_data"]
filtered_results_collection = db["filtered_deseq2_results"]

def test_filter_significant_genes():
    """
    Test filtering of DESeq2 results by p-value and fold-change.
    """
    # Filter DESeq2 results
    significant_genes = filter_significant_genes(sample_deseq2_results)

    # Check the filtering output
    assert len(significant_genes) == 3  # Three genes should meet the threshold
    assert "Gene1" in significant_genes["gene"].values

    # Insert results into MongoDB and verify insertion
    filtered_results_collection.insert_many(significant_genes.to_dict('records'))
    db_filtered_count = filtered_results_collection.count_documents({})
    assert db_filtered_count > 0  # Ensure filtered results were inserted into MongoDB

    # Cleanup MongoDB after test
    filtered_results_collection.delete_many({})

def test_save_filtered_results(tmp_path):
    """
    Test saving filtered results to CSV.
    """
    # Use a temporary path for output
    output_file = tmp_path / "filtered_genes.csv"

    # Filter and save results
    significant_genes = filter_significant_genes(sample_deseq2_results)
    save_filtered_results(significant_genes, output_file)

    # Verify CSV file exists and contains data
    saved_data = pd.read_csv(output_file)
    assert len(saved_data) == 3  # Should match the filtered results count
    assert "Gene1" in saved_data["gene"].values  # Verify content
