# main.py

from rna_seq_pipeline.deseq2_pipeline import run_deseq2
from ml_pipeline.process_deseq2_results import filter_significant_genes, save_filtered_results_to_csv
from data_fetching import fetch_expression_data, fetch_sample_info

# Fetch expression data and sample metadata
expression_data = fetch_expression_data()
sample_info = fetch_sample_info()

# Run DESeq2 Analysis
deseq2_results = run_deseq2(expression_data, sample_info)

# Filter significant results for ML
significant_genes = filter_significant_genes(deseq2_results)
save_filtered_results_to_csv(significant_genes, 'data/significant_genes.csv')
