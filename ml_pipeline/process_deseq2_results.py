# ml_pipeline/process_deseq2_results.py

import os
import pandas as pd

def filter_significant_genes(deseq2_results, padj_threshold=0.05, log2fc_threshold=1):
    """
    Filter DESeq2 results for genes that meet significance and fold-change criteria.
    """
    # Filter based on adjusted p-value and log2 fold-change
    significant_genes = deseq2_results[
        (deseq2_results['padj'] < padj_threshold) & 
        (abs(deseq2_results['log2FoldChange']) >= log2fc_threshold)
    ]
    return significant_genes

def save_filtered_results(significant_genes, output_file):
    """
    Save filtered DESeq2 results to a CSV file.
    """
    if os.path.exists(output_file):
        print(f"Warning: {output_file} already exists and will be overwritten.")
    significant_genes.to_csv(output_file, index=False)

# Example usage
if __name__ == "__main__":
    # Load DESeq2 results (assuming these have already been generated)
    deseq2_results = pd.read_csv('data/deseq2_results.csv')
    
    # Filter results for significant genes
    significant_genes = filter_significant_genes(deseq2_results)
    
    # Save filtered results
    save_filtered_results(significant_genes, 'data/significant_genes.csv')
