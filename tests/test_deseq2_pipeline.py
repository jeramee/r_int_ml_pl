# tests/test_deseq2_pipeline.py

import pytest
import pandas as pd
from unittest.mock import patch
from rna_seq_pipeline.deseq2_pipeline import run_deseq2
from pymongo import MongoClient

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
