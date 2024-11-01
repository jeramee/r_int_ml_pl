# Core Libraries for Data Processing and Parallel Execution
library(Rcpp)           # Core dependency for JIT and Rcpp functionality
library(rlang)          # Dependency for 'parallelly' and 'DESeq2'
library(parallelly)     # Needed for future
library(future)         # Task scheduling and parallel processing
library(Matrix)         # Common dependency in bioinformatics packages
library(DESeq2)         # Core bioinformatics package

# Additional Data Processing and Workflow Libraries
library(gettext)
library(broom)          # For tidying model outputs
library(dbplyr)         # Database backend for dplyr
library(knitr)          # For creating dynamic reports
library(recipes)        # Data preprocessing for modeling
library(future)         # (Duplicate to ensure correct version is loaded)
library(googledrive)    # Access to Google Drive API
library(googlesheets4)  # Access to Google Sheets API

install.packages("Rcpp", type = "binary")
install.packages("Matrix", type = "binary")
install.packages("parallelly", type = "binary")


# Install packages if they are missing or need updates
required_packages <- c(
  "Rcpp", "rlang", "parallelly", "future", "Matrix", "DESeq2", 
  "broom", "dbplyr", "knitr", "recipes", "googledrive", "googlesheets4"
)

install_if_missing <- function(pkg) {
  if (!requireNamespace(pkg, quietly = TRUE)) {
    install.packages(pkg)
  }
}

# Install all required packages that are missing
invisible(sapply(required_packages, install_if_missing))

# Print confirmation message
print("R libraries loaded and installed successfully")
