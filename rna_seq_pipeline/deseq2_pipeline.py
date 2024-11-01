# rna_seq_pipeline/deseq2_pipeline.py

import sys
import os
import pandas as pd
import threading

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

# Increase stack size
threading.stack_size(2 * 1024 * 1024)

import rpy2.robjects as ro

# Ensure gettext override is called first
# ro.r('source("../gettext_override.R")')
ro.r('source("D:/000_AI_Helper/000_Do_Informatics/Final_info_controller/InfoProj_CG_PTTD_CTS/flow-forge/pipeline_interface/r_int_ml_pl/gettext_override.R")')


# Import rpy2 components after gettext override
from rpy2.robjects import pandas2ri
from rpy2.robjects.conversion import localconverter
from rpy2.robjects.packages import importr
from rpy2.robjects.vectors import StrVector, IntVector, FloatVector

# Activate pandas-to-R DataFrame conversion
pandas2ri.activate()

# Load base and DESeq2 after importing gettext override
base = importr('base')
deseq2 = importr('DESeq2')

'''
try:
    import rpy2.robjects as ro

    # Ensure gettext override is called first
    ro.r('source("../gettext_override.R")')

    # Import rpy2 components after gettext override
    from rpy2.robjects import pandas2ri
    from rpy2.robjects.conversion import localconverter
    from rpy2.robjects.packages import importr
    from rpy2.robjects.vectors import StrVector, IntVector, FloatVector

    # Activate pandas-to-R DataFrame conversion
    pandas2ri.activate()

    # Load base and DESeq2 after importing gettext override
    base = importr('base')
    deseq2 = importr('DESeq2')

except Exception as e:
    print(f"R initialization error: {e}")
'''

def run_deseq2(expression_data, sample_info):
    """
    Perform DESeq2 analysis on RNA-Seq count data.

    Args:
        expression_data (pd.DataFrame): Count data for genes (rows) across samples (columns).
        sample_info (pd.DataFrame): Sample metadata with conditions.

    Returns:
        pd.DataFrame: DESeq2 analysis results with differential expression stats.
    """
    # Ensure gene names are row indices in expression data and samples are row indices in sample_info
    expression_data.index.name = 'gene'
    sample_info.index = expression_data.columns

    # Convert the 'condition' column in sample_info to a categorical type
    if 'condition' in sample_info.columns:
        sample_info['condition'] = sample_info['condition'].astype('category')

    # Convert pandas DataFrames to R-compatible DataFrames using pandas2ri converter
    with localconverter(pandas2ri.converter):
        expression_data_r = pandas2ri.py2rpy(expression_data)
        sample_info_r = pandas2ri.py2rpy(sample_info)

    # Assign R variables for DESeq2 analysis
    ro.globalenv['expression_data'] = expression_data_r
    ro.globalenv['sample_info'] = sample_info_r

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
    with localconverter(pandas2ri.converter):
        deseq2_results = pandas2ri.rpy2py(deseq2_results_r)
    return deseq2_results
