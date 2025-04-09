# LlamaCancer Documentation

Welcome to the LlamaCancer documentation. This directory contains comprehensive documentation for the LlamaCancer package, a Python framework for analyzing biomarker associations in oncology clinical trials.

## Documentation Overview

- **User Guide**: Instructions for installation, configuration, and basic usage of LlamaCancer
- **API Reference**: Detailed documentation of LlamaCancer modules, classes, and functions
- **Examples**: Code examples and Jupyter notebooks demonstrating LlamaCancer workflows
- **Tutorials**: Step-by-step tutorials for common biomarker analysis tasks

## User Guide

### Installation

```bash
# Install from PyPI (when published)
pip install llamacancer

# Install from source
git clone https://github.com/yourusername/llamacancer.git
cd llamacancer
pip install -e .
```

### Quick Start

```python
import llamacancer as lc
from llamacancer.config import load_config
from llamacancer.io import load_clinical_data, load_biomarker_data, merge_clinical_biomarkers
from llamacancer.analysis import run_biomarker_associations

# Load configuration
config = load_config("path/to/config.py")

# Load and merge data
clinical_df = load_clinical_data(config)
biomarker_df = load_biomarker_data(config)
merged_df = merge_clinical_biomarkers(clinical_df, biomarker_df)

# Run biomarker association analysis
results = run_biomarker_associations(merged_df, config)

# Display significant biomarkers
print(f"Significant biomarkers: {results['summary']['significant_biomarkers']}")
```

## Core Concepts

### Configuration

LlamaCancer uses a configuration-based approach for defining analysis parameters. A configuration file specifies data locations, endpoint definitions, biomarker cutoffs, and analysis settings.

Example configuration:

```python
# configs/my_analysis_config.py
from ml_collections import config_dict

def get_config():
    config = config_dict.ConfigDict()
    
    # General settings
    config.project_name = "My Biomarker Analysis"
    config.data_dir = "data/"
    config.results_dir = "results/"
    
    # File paths & core columns
    config.clinical_file = "clinical_data.csv"
    config.biomarker_files = {
        "primary": "biomarker_data.csv",
    }
    config.subject_id_col = "PatientID"
    
    # Endpoint definitions
    config.endpoints = config_dict.ConfigDict()
    config.endpoints.event_free_survival = config_dict.ConfigDict()
    config.endpoints.event_free_survival.time_col = "EFS_Time_Months"
    config.endpoints.event_free_survival.status_col = "EFS_Event_Status"
    
    # Biomarkers to analyze
    config.biomarkers_to_analyze = [
        "B_cell_GES",
        "CD19_Expression_Level",
    ]
    
    return config
```

### Data Structure

LlamaCancer expects your clinical and biomarker data to be in CSV format with a common patient identifier.

Example clinical data:
```
PatientID,TreatmentArm,EFS_Time_Months,EFS_Event_Status
P001,CART,15.2,0
P002,SOC,8.7,1
```

Example biomarker data:
```
PatientID,B_cell_GES,CD19_Expression_Level
P001,8.76,High
P002,5.43,Low
```

### Analysis Workflow

The typical LlamaCancer workflow involves:

1. **Loading data**: Loading clinical and biomarker data
2. **Merging data**: Combining patient clinical data with biomarker measurements
3. **Endpoint extraction**: Extracting survival or response endpoints
4. **Biomarker processing**: Converting continuous biomarkers to categorical (high/low) groups
5. **Statistical analysis**: Performing statistical tests to assess biomarker associations
6. **Visualization**: Generating plots for individual biomarkers and summary plots
7. **Interpretation**: Analyzing the findings and drawing conclusions

## API Reference

For detailed API documentation, see the [API Reference](api_reference.md) document.

## Examples

The `notebooks/` directory contains Jupyter notebooks demonstrating various LlamaCancer workflows:

- `1_biomarker_association_workflow.ipynb`: Basic biomarker association analysis workflow
- `2_biomarker_interaction_analysis.ipynb`: Analysis of biomarker interactions
- `3_multivariate_analysis.ipynb`: Multivariate analysis of biomarkers

## License

LlamaCancer is released under the MIT License. See the LICENSE file for details.
