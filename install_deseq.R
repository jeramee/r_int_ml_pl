if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("DESeq2")

# Install other necessary packages from CRAN if not available via Bioconductor
install.packages(c("Rcpp", "rlang", "parallelly", "future", "Matrix"))
install.packages(c("broom", "dbplyr", "knitr", "gettext"))
install.packages(c("recipes", "googledrive", "googlesheets4"))

# Load the installed libraries to check if they were installed successfully
library(DESeq2)
library(Rcpp)
library(rlang)
library(parallelly)
library(future)
library(Matrix)
print("All libraries loaded successfully.")