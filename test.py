# test.py

import os
import subprocess

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

'''
# Verify paths
print("PATH:", os.environ["PATH"])
print("R_HOME:", os.environ["R_HOME"])
print("LD_LIBRARY_PATH:", os.environ.get("LD_LIBRARY_PATH"))
'''

# Import rpy2 after setting paths
import rpy2.robjects as robjects

# Test R connectivity and load gettext_override.R
try:
    print("R Version:", robjects.r('R.version.string')[0])
    
    # Source gettext_override.R to override gettext functions
    robjects.r('source("gettext_override.R")')
    print("gettext_override.R sourced successfully.")

    # Load required libraries to confirm they are present
    libraries = [
        "Rcpp", "rlang", "parallelly", "future", "Matrix", "DESeq2",
        "gettext", "broom", "dbplyr", "knitr", "recipes", "googledrive", "googlesheets4"
    ]

    for lib in libraries:
        robjects.r(f'library({lib})')
        print(f"Library {lib} loaded successfully.")

    # Test custom gettext functions
    gettext_result = robjects.r('gettext("Hello World")')[0]
    ngettext_result = robjects.r('ngettext("There is one item", "There are multiple items", 2)')[0]

    print("gettext result:", gettext_result)
    print("ngettext result:", ngettext_result)

except Exception as e:
    print(f"Error: {e}")

# Run a simple R script to confirm environment functionality
subprocess.run(["Rscript", "-e", 'print("R environment is functioning as expected.")'])
