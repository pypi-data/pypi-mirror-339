#!/usr/bin/env python
# coding: utf-8

# # LlamaCancer: Biomarker Association Analysis Workflow
#
# This notebook demonstrates how to use the LlamaCancer package to analyze biomarker associations with clinical endpoints in oncology trials.
#
# ## Workflow Overview
#
# 1. **Data Loading**: Import clinical and biomarker data
# 2. **Data Merging**: Combine patient clinical data with biomarker measurements
# 3. **Endpoint Definition**: Define survival, response, and other endpoints
# 4. **Biomarker Dichotomization**: Convert continuous biomarkers to High/Low groups
# 5. **Association Analysis**: Perform statistical tests to assess biomarker associations
# 6. **Visualization**: Generate plots for individual biomarkers and summary plots
# 7. **Result Interpretation**: Analyze the findings and draw conclusions

# In[1]:


# Import standard libraries
import os
from typing import Any, Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Set plotting style
plt.style.use("seaborn-v0_8-whitegrid")

# For notebook display
get_ipython().run_line_magic("matplotlib", "inline")
plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["figure.dpi"] = 100


# In[2]:


# Import LlamaCancer modules
# Make sure the package is in your Python path
import sys

sys.path.append("..")

from llamacancer.analysis import _dichotomize_biomarker, run_biomarker_associations
from llamacancer.config import load_config
from llamacancer.endpoints import get_endpoint_data, get_response_data
from llamacancer.io import load_biomarker_data, load_clinical_data, merge_clinical_biomarkers
from llamacancer.stats import fisher_exact_test, fit_coxph_model, run_logrank_test
from llamacancer.utils import setup_logging
from llamacancer.vis import plot_forest, plot_kaplan_meier, plot_volcano

# Setup logging
setup_logging(level="INFO")


# ## 1. Configuration and Data Loading
#
# First, we'll load the configuration that defines our analysis parameters and load our sample data.

# In[3]:


# Load configuration
config = load_config("../configs/default_analysis_config.py")

# Display key configuration settings
print(f"Project: {config.project_name}")
print(f"Data directory: {config.data_dir}")
print(f"Primary endpoint: {config.primary_endpoint}")
print(f"Biomarkers to analyze:")
for biomarker in config.biomarkers_to_analyze:
    print(f"- {biomarker}")


# In[4]:


# Load clinical data
clinical_df = load_clinical_data(config)
print(f"Clinical data shape: {clinical_df.shape}")
clinical_df.head()


# In[5]:


# Load biomarker data
biomarker_df = load_biomarker_data(config)
print(f"Biomarker data shape: {biomarker_df.shape}")
biomarker_df.head()


# In[6]:


# Merge the datasets
merged_df = merge_clinical_biomarkers(clinical_df, biomarker_df)
print(f"Merged data shape: {merged_df.shape}")

# Check the first few rows
merged_df.head()


# ## 2. Data Exploration
#
# Let's explore the distributions of our key clinical endpoints and biomarkers.

# In[7]:


# Treatment arm distribution
treatment_counts = merged_df[config.treatment_arm_col].value_counts()
plt.figure(figsize=(8, 6))
treatment_counts.plot(kind="bar")
plt.title("Distribution of Treatment Arms")
plt.ylabel("Number of Patients")
plt.grid(axis="y", alpha=0.3)
plt.show()

# Show the counts
print("Treatment Arm Counts:")
print(treatment_counts)


# In[8]:


# Response outcome distribution
if hasattr(config.endpoints, "response") and hasattr(config.endpoints.response, "response_col"):
    response_col = config.endpoints.response.response_col
    response_counts = merged_df[response_col].value_counts()

    plt.figure(figsize=(10, 6))
    response_counts.plot(kind="bar")
    plt.title(f"Distribution of {response_col}")
    plt.ylabel("Number of Patients")
    plt.grid(axis="y", alpha=0.3)
    plt.show()

    # Show the counts
    print(f"{response_col} Counts:")
    print(response_counts)


# In[9]:


# Plot distributions of continuous biomarkers
continuous_biomarkers = [
    b
    for b in config.biomarkers_to_analyze
    if b in merged_df.columns and pd.api.types.is_numeric_dtype(merged_df[b])
]

if continuous_biomarkers:
    # Create a multi-panel plot
    n_cols = 2
    n_rows = (len(continuous_biomarkers) + 1) // 2
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(14, 4 * n_rows))
    axes = axes.flatten()

    for i, biomarker in enumerate(continuous_biomarkers):
        if i < len(axes):
            sns.histplot(merged_df[biomarker].dropna(), kde=True, ax=axes[i])
            axes[i].set_title(f"Distribution of {biomarker}")
            axes[i].set_xlabel(biomarker)
            axes[i].set_ylabel("Count")

    # Hide any unused subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    plt.show()
