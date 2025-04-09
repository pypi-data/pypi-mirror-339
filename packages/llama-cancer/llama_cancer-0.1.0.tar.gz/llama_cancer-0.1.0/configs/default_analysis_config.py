# configs/default_analysis_config.py
from ml_collections import config_dict


def get_config():
    """Default configuration for LlamaCancer analysis."""
    config = config_dict.ConfigDict()

    # === General Settings ===
    config.project_name = "LlamaCancer_Analysis"
    config.data_dir = "data/sample_data/"
    config.results_dir = "results/"
    config.seed = 42

    # === File Paths & Core Columns ===
    config.clinical_file = "clinical_data.csv"
    config.biomarker_files = {
        "primary": "biomarker_data.csv",
    }
    config.subject_id_col = "PatientID"
    config.treatment_arm_col = "TreatmentArm"
    config.primary_comparison_arms = ["CART", "SOC"]

    # === Endpoint Definitions ===
    config.endpoints = config_dict.ConfigDict()
    config.endpoints.event_free_survival = config_dict.ConfigDict()
    config.endpoints.event_free_survival.time_col = "EFS_Time_Months"
    config.endpoints.event_free_survival.status_col = "EFS_Event_Status"
    config.endpoints.event_free_survival.unit = "Months"
    config.endpoints.overall_survival = config_dict.ConfigDict()
    config.endpoints.overall_survival.time_col = "OS_Time_Months"
    config.endpoints.overall_survival.status_col = "OS_Event_Status"
    config.endpoints.overall_survival.unit = "Months"
    config.endpoints.response = config_dict.ConfigDict()
    config.endpoints.response.response_col = "BestOverallResponse"
    config.endpoints.response.positive_values = ["CR", "PR", "Ongoing Response"]
    config.endpoints.response.type = "categorical"

    # === Biomarkers to Analyze ===
    config.biomarkers_to_analyze = [
        "B_cell_GES",
        "Stromal_SII_Score",
        "CD19_Expression_Level",
        "CD19_HScore",
        "APM_Score",
        "PDL1_Status",
    ]
    config.biomarker_cutoffs = {
        "B_cell_GES": "median",
        "Stromal_SII_Score": "median",
        "CD19_HScore": 150,
        "APM_Score": "quartile",
    }
    config.biomarker_positive_categories = {
        "CD19_Expression_Level": "High",
        "PDL1_Status": "Positive",
    }

    # === Analysis Settings ===
    config.primary_endpoint = "event_free_survival"
    config.association_stat_survival = "CoxPH"
    config.association_stat_binary = "LogisticRegression"
    config.group_comparison_stat_continuous = "MannWhitneyU"
    config.group_comparison_stat_categorical = "ChiSquare"
    config.correlation_method = "spearman"
    config.alpha_threshold = 0.05

    # === Plotting Settings ===
    config.plot_style = "seaborn-v0_8-whitegrid"
    config.plot_palette = "viridis"
    config.plot_dpi = 150
    config.plot_format = "png"
    config.km_plot_conf_int = True
    config.km_plot_at_risk = True
    config.volcano_plot_log10_pval = True

    return config
