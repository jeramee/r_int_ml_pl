# deseq2_analysis.py

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

try:
    import rpy2.robjects as ro

    # Ensure gettext override is called first
    ro.r('source("../gettext_override.R")')

    # Import rpy2 components after gettext override
    from rpy2.robjects import pandas2ri
    from rpy2.robjects.packages import importr

    # Activate pandas-to-R DataFrame conversion
    pandas2ri.activate()

    # Load base and DESeq2 after importing gettext override
    base = importr('base')
    deseq2 = importr('DESeq2')

except Exception as e:
    print(f"R initialization error: {e}")

# Assume `expression_data` and `sample_info` are pandas DataFrames
expression_data_r = pandas2ri.py2rpy(expression_data)
sample_info_r = pandas2ri.py2rpy(sample_info)

# Run DESeq2 analysis
ro.r('''
dds <- DESeqDataSetFromMatrix(countData = expression_data,
                              colData = sample_info,
                              design = ~ condition)
dds <- DESeq(dds)
res <- results(dds)
''')

# Convert results back to pandas DataFrame
deseq2_results_r = ro.r('as.data.frame(res)')
deseq2_results = pandas2ri.rpy2py(deseq2_results_r)
print(deseq2_results.head())
