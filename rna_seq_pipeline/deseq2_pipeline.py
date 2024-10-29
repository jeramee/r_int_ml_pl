# rna_seq_pipeline/deseq2_pipeline.py

import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

# Activate pandas-to-R DataFrame conversion
pandas2ri.activate()

# Load DESeq2 in R
base = importr('base')
deseq2 = importr('DESeq2')

def run_deseq2(expression_data, sample_info):
    """
    Perform DESeq2 analysis on RNA-Seq count data.
    
    Args:
        expression_data (pd.DataFrame): Count data for genes (rows) across samples (columns).
        sample_info (pd.DataFrame): Sample metadata with conditions.
    
    Returns:
        pd.DataFrame: DESeq2 analysis results with differential expression stats.
    """
    # Convert pandas DataFrames to R objects
    expression_data_r = pandas2ri.py2rpy(expression_data)
    sample_info_r = pandas2ri.py2rpy(sample_info)

    # Run DESeq2 analysis in R
    ro.r('''
    dds <- DESeqDataSetFromMatrix(countData = expression_data,
                                  colData = sample_info,
                                  design = ~ condition)
    dds <- DESeq(dds)
    res <- results(dds)
    ''')

    # Convert DESeq2 results to pandas DataFrame
    deseq2_results_r = ro.r('as.data.frame(res)')
    deseq2_results = pandas2ri.rpy2py(deseq2_results_r)
    return deseq2_results
