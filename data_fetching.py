# data_fetching.py

import pandas as pd

def fetch_expression_data():
    """
    Placeholder function for fetching expression data (count data).
    Replace with API calls to GEO, TCGA, or load from file.
    """
    return pd.read_csv('data/expression_data.csv')

def fetch_sample_info():
    """
    Placeholder function for fetching sample metadata.
    Replace with API calls to GEO, TCGA, or load from file.
    """
    return pd.read_csv('data/sample_info.csv')
