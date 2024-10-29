# r_int_ml_pl
## R Integration Machine Learning Pipeline

### DESeq2 Pipeline Integration (rpy2-based) for RNA-Seq Analysis

This pipeline provides RNA-Seq differential expression analysis capabilities using DESeq2 through the rpy2 interface. It is structured to operate seamlessly within the project’s larger data processing framework, enabling integration with both Python-based bioinformatics and cheminformatics modules.

## Pipeline Overview

The DESeq2 pipeline leverages rpy2 to call R functions within Python, allowing users to run DESeq2’s statistical analysis on gene expression data directly. This setup is ideal for cancer genomics studies, such as analyzing differential expression in ALK-positive cancers. Below is an overview of each step and how it complements the larger project:

1. **Data Conversion**: Converts pandas DataFrames to R-compatible formats for use in R functions, enabling smooth data handling between Python and R.
2. **DESeq2 Analysis**: Runs DESeq2 differential expression analysis using count and sample data provided in Python, returning significant genes and fold change values.
3. **Results Integration**: Outputs DESeq2 results as a pandas DataFrame, ready for downstream Python-based ML pipelines, visualization, or additional bioinformatics processing.

## Implementation Steps

### 1. Load Data and Libraries
- Use rpy2 to bridge Python and R, allowing DESeq2 functions to be called within the Python environment.
- Activate `pandas2ri` for automatic conversion between pandas DataFrames (Python) and R DataFrames.

```python
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

# Activate pandas-to-R DataFrame conversion
pandas2ri.activate()
```

## 2. Set Up DESeq2 in R

- **Load DESeq2 and Base R Packages**
- Ensure `expression_data` and `sample_info` are pandas DataFrames containing RNA-Seq count data and sample information, respectively.

```python
from rpy2.robjects import pandas2ri
from rpy2.robjects.packages import importr

base = importr('base')
deseq2 = importr('DESeq2')
expression_data_r = pandas2ri.py2rpy(expression_data)
sample_info_r = pandas2ri.py2rpy(sample_info)
```

## 3. Run DESeq2 Analysis

Use DESeq2’s `DESeqDataSetFromMatrix` and `DESeq` functions to perform differential expression analysis based on sample conditions.

```python

import rpy2.robjects as ro

ro.r('''
dds <- DESeqDataSetFromMatrix(countData = expression_data,
                              colData = sample_info,
                              design = ~ condition)
dds <- DESeq(dds)
res <- results(dds)
''')
```

## 4. Retrieve and Process Results

Convert DESeq2 results to a pandas DataFrame for compatibility with other Python tools and machine learning pipelines.

```python
deseq2_results_r = ro.r('as.data.frame(res)')
deseq2_results = pandas2ri.rpy2py(deseq2_results_r)
print(deseq2_results.head())
```

## Pipeline Structure

The DESeq2 pipeline module is designed to be compatible with the larger project structure, allowing for easy data retrieval, processing, and integration with ML pipelines.

## Project Structure

```plaintext

project_root/
│
├── rna_seq_pipeline/                # DESeq2 Pipeline Integration
│   ├── deseq2_pipeline.py           # DESeq2 interface module
│
├── data/                            # Data directory
│   ├── expression_data.csv          # Example expression count data
│   └── sample_info.csv              # Example sample metadata
│
├── ml_pipeline/                     # ML Modules for post-processing
│   ├── process_deseq2_results.py    # Integrate DESeq2 results for ML tasks
│
└── README.md                        # Project documentation
```

## Key Benefits

- **Flexible Integration:** Can handle data directly from GEO or TCGA pipelines, making it compatible with existing genomic data workflows.
- **Statistical Rigor:** DESeq2 is highly regarded for RNA-Seq analysis, offering reliable differential expression results based on robust statistical methods.
- **Seamless Data Transfer:** rpy2 ensures data remains compatible across platforms, allowing efficient transfer between Python data pipelines and R statistical tools.

This pipeline is released as part of Phase 1.5, following foundational implementations in Phase 1.0 and adding enhanced genomic data processing capabilities alongside other chemical and genomic data tools.

### License

This project is licensed under the MIT License.
