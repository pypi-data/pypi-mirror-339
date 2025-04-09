# LlamaCancer Analysis Module

The `llamacancer.analysis` module provides functions for performing biomarker association analyses in oncology clinical trials.

## API Reference

### run_biomarker_associations

```python
def run_biomarker_associations(df: pd.DataFrame, config: Any) -> Dict[str, Any]:
    """
    Run comprehensive biomarker association analyses.
    
    Args:
        df: DataFrame containing clinical and biomarker data
        config: Configuration object with analysis parameters
        
    Returns:
        Dictionary containing analysis results structured as:
        {
            'survival': {biomarker_name: survival_results, ...},
            'response': {biomarker_name: response_results, ...},
            'summary': {
                'num_biomarkers_analyzed': int,
                'significant_biomarkers': List[str],
                'execution_time': float
            }
        }
    """
```

This function is the main entry point for running biomarker association analyses. It performs the following tasks:

1. Iterates through each biomarker specified in `config.biomarkers_to_analyze`
2. Dichotomizes continuous biomarkers based on cutoffs defined in config
3. Performs survival analyses (log-rank test, Cox PH model) and response analyses (Fisher's exact test) as applicable
4. Generates visualizations for each biomarker (Kaplan-Meier plots, etc.)
5. Compiles results into a structured dictionary with detailed statistics and visualizations
6. Generates summary statistics and identifies significant biomarkers

### _dichotomize_biomarker

```python
def _dichotomize_biomarker(df: pd.DataFrame, biomarker: str, config: Any) -> pd.DataFrame:
    """
    Dichotomize a biomarker based on the configuration settings.
    
    Args:
        df: DataFrame containing the biomarker
        biomarker: Name of the biomarker column
        config: Configuration object specifying cutoff methods
        
    Returns:
        DataFrame with an additional column '{biomarker}_group' containing the dichotomized values
    """
```

This function converts continuous biomarkers to categorical (high/low) groups based on configuration settings. The dichotomization can be done using different methods:

- **median**: Split at the median value
- **mean**: Split at the mean value
- **quartile**: Create three groups (Low, Mid, High) based on quartiles
- **fixed value**: Split at a specified threshold
- **positive categories**: For categorical biomarkers, specify which values should be considered "positive"

The function adds a new column to the DataFrame with the suffix `_group` containing the dichotomized values.

### _analyze_survival_by_biomarker

```python
def _analyze_survival_by_biomarker(
    df: pd.DataFrame, 
    biomarker: str, 
    group_col: str, 
    endpoint: str,
    config: Any
) -> Dict[str, Any]:
    """
    Analyze survival outcomes for a dichotomized biomarker.
    
    Args:
        df: DataFrame containing the biomarker and survival data
        biomarker: Original biomarker name
        group_col: Column name for the dichotomized biomarker groups
        endpoint: Endpoint name (e.g., 'event_free_survival')
        config: Configuration object
        
    Returns:
        Dictionary containing analysis results including:
        - log-rank test results
        - Cox proportional hazards model results
        - Kaplan-Meier plot path
    """
```

This function performs survival analysis for a given biomarker, including:

1. Running log-rank tests to compare survival between biomarker groups
2. Fitting Cox proportional hazards models to estimate hazard ratios
3. Generating Kaplan-Meier plots
4. Computing concordance index and other model metrics

### _analyze_response_by_biomarker

```python
def _analyze_response_by_biomarker(
    df: pd.DataFrame, 
    biomarker: str, 
    group_col: str, 
    config: Any
) -> Dict[str, Any]:
    """
    Analyze response outcomes for a dichotomized biomarker.
    
    Args:
        df: DataFrame containing the biomarker and response data
        biomarker: Original biomarker name
        group_col: Column name for the dichotomized biomarker groups
        config: Configuration object
        
    Returns:
        Dictionary containing analysis results including:
        - Fisher's exact test results
        - Contingency table
        - Bar plot path
    """
```

This function analyzes the association between biomarker groups and response outcomes, including:

1. Creating contingency tables of biomarker groups vs. response
2. Running Fisher's exact test to assess statistical significance
3. Calculating odds ratios and confidence intervals
4. Generating bar plots to visualize response rates by biomarker group

## Examples

### Basic Biomarker Association Analysis

```python
from llamacancer.config import load_config
from llamacancer.io import load_clinical_data, load_biomarker_data, merge_clinical_biomarkers
from llamacancer.analysis import run_biomarker_associations

# Load configuration and data
config = load_config("configs/default_analysis_config.py")
clinical_df = load_clinical_data(config)
biomarker_df = load_biomarker_data(config)
merged_df = merge_clinical_biomarkers(clinical_df, biomarker_df)

# Run biomarker association analysis
results = run_biomarker_associations(merged_df, config)

# Display significant biomarkers
print(f"Analysis completed for {results['summary']['num_biomarkers_analyzed']} biomarkers")
print(f"Significant biomarkers: {results['summary']['significant_biomarkers']}")

# Access results for a specific biomarker
biomarker = "B_cell_GES"
if biomarker in results['survival']:
    print(f"Hazard ratio for {biomarker}: {results['survival'][biomarker]['cox_results']['hazard_ratio']:.2f}")
    print(f"P-value: {results['survival'][biomarker]['cox_results']['p_value']:.4f}")
```

### Manual Biomarker Dichotomization

```python
from llamacancer.analysis import _dichotomize_biomarker

# Dichotomize a biomarker at the median
df_with_groups = _dichotomize_biomarker(merged_df, "B_cell_GES", config)

# Check the distribution of groups
group_col = "B_cell_GES_group"
print(df_with_groups[group_col].value_counts())
``` 