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
