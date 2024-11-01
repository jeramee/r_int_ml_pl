# py_fix_r.py

import os
import rpy2.robjects as robjects

# Set R_HOME to your conda environment's R path
os.environ["R_HOME"] = r"C:\Users\jeram\miniconda3\envs\myenv_py38"

# Add R binary from the x64 folder and Rtools40 to PATH
os.environ["PATH"] += r";C:\Users\jeram\miniconda3\envs\myenv_py38\Library\bin\x64"
os.environ["PATH"] += r";C:\rtools40\usr\bin"

# Verify Rtools setup by checking "make" availability
make_path = robjects.r('Sys.which("make")')
print("Make path:", make_path)

# Verify R version to confirm integration
print(robjects.r("R.version.string"))
