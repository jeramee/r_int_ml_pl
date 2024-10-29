# tests/test_process_deseq2_results.py

import pytest
import pandas as pd
from ml_pipeline.process_deseq2_results import filter_significant_genes, save_filtered_results_to_csv
from pymongo import MongoClient

# Sample DESeq2 results data
sample_deseq2_results = pd.DataFrame({
    "gene": ["Gene1", "Gene2", "Gene3"],
    "log2FoldChange": [1.5, -2.3, 0.8],
    "padj": [0.01, 0.03, 0.2]
})

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
    assert len(significant_genes) == 2  # Two genes should meet the threshold
    assert "Gene1" in significant_genes["gene"].values

    # Check MongoDB insertion
    db_filtered_count = filtered_results_collection.count_documents({})
    assert db_filtered_count > 0  # Ensure filtered results were inserted into MongoDB

    # Cleanup MongoDB after test
    filtered_results_collection.delete_many({})

def test_save_filtered_results_to_csv(tmp_path):
    """
    Test saving filtered results to CSV.
    """
    # Use a temporary path for output
    output_file = tmp_path / "filtered_genes.csv"

    # Filter and save results
    significant_genes = filter_significant_genes(sample_deseq2_results)
    save_filtered_results_to_csv(significant_genes, output_file)

    # Verify CSV file exists and contains data
    saved_data = pd.read_csv(output_file)
    assert len(saved_data) == 2  # Should match the filtered results count
