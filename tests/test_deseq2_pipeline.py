# tests/test_deseq2_pipeline.py

import os
import sys
import pytest
import pandas as pd
from unittest.mock import patch
from pymongo import MongoClient

# Add the parent directory of 'ml_pipeline' to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

# Set environment variables
os.environ["PATH"] += r";C:\Users\jeram\miniconda3\envs\myenv_py38\Lib\R\bin"
os.environ["PATH"] += r";C:\Users\jeram\miniconda3\envs\myenv_py38\Lib\R\bin\x64"
os.environ["R_HOME"] = r"C:\Users\jeram\miniconda3\envs\myenv_py38\Lib\R"
os.environ["R_LIBS_USER"] = r"C:\Users\jeram\miniconda3\envs\myenv_py38\Lib\R\library"
os.environ["LD_LIBRARY_PATH"] = r"C:\Users\jeram\miniconda3\envs\myenv_py38\lib\R\lib"

# Disable R's bytecode compilation for this session
os.environ["R_COMPILE_PKGS"] = "0"

try:
    import rpy2.robjects as ro
    ro.r('source("../gettext_override.R")')
except Exception as e:
    print(f"R initialization error: {e}")

from rna_seq_pipeline.deseq2_pipeline import run_deseq2

# Sample test data
sample_expression_data = pd.DataFrame({
    "Gene1": [100, 150, 80],
    "Gene2": [200, 190, 210],
    "Gene3": [50, 60, 55]
})
sample_metadata = pd.DataFrame({
    "condition": ["control", "treatment", "control"]
})

# MongoDB setup
client = MongoClient("mongodb://localhost:27017/")
db = client["rna_seq_data"]
results_collection = db["deseq2_results"]

def test_run_deseq2():
    """
    Test DESeq2 execution and MongoDB integration.
    """
    # Run DESeq2 analysis
    deseq2_results = run_deseq2(sample_expression_data, sample_metadata)

    # Check results DataFrame is not empty
    assert not deseq2_results.empty

    # Check MongoDB insertion
    db_result_count = results_collection.count_documents({})
    assert db_result_count > 0  # Ensure results were inserted into MongoDB

    # Cleanup MongoDB after test
    results_collection.delete_many({})
