# main.py
import argparse
import logging
import sys

from llamacancer.config import load_config
from llamacancer.endpoints import get_endpoint_data
from llamacancer.io import (
    load_biomarker_data,
    load_clinical_data,
    merge_clinical_biomarkers,
)
from llamacancer.stats import run_logrank_test
from llamacancer.utils import setup_logging
from llamacancer.vis import plot_kaplan_meier


def main():
    parser = argparse.ArgumentParser(description="Run LlamaCancer Analysis Pipeline")
    parser.add_argument(
        "--config",
        type=str,
        default="configs/default_analysis_config.py",
        help="Path to config file.",
    )
    args = parser.parse_args()

    # Set up logging
    setup_logging(level="INFO")

    # Load configuration
    config = load_config(args.config)
    logging.info("Configuration loaded.")

    # Load clinical data
    clinical_df = load_clinical_data(config)
    if clinical_df is None:
        logging.error("Clinical data failed to load. Exiting.")
        sys.exit(1)

    # Load biomarker data
    biomarker_df = load_biomarker_data(config)

    # Merge datasets
    merged_df = merge_clinical_biomarkers(clinical_df, biomarker_df)
    logging.info(f"Merged data shape: {merged_df.shape}")

    # Extract endpoint data (example: event_free_survival)
    endpoint = config.primary_endpoint
    duration, event = get_endpoint_data(merged_df, endpoint, config)
    if duration is None or event is None:
        logging.error("Failed to extract endpoint data. Exiting.")
        sys.exit(1)

    # Run survival analysis (e.g., Log-Rank test between primary treatment arms)
    group_col = config.treatment_arm_col
    test_results = run_logrank_test(duration, event, merged_df[group_col])
    if test_results:
        logging.info(f"Logrank test results: {test_results}")

    # Generate Kaplan-Meier plot
    plot_kaplan_meier(
        df=merged_df,
        duration_col=config.endpoints[endpoint].time_col,
        event_col=config.endpoints[endpoint].status_col,
        group_col=group_col,
        config=config,
        filename="kaplan_meier_example.png",
        test_results=test_results,
    )

    # (Placeholder) Additional analyses and visualizations can be added here.
    logging.info("LlamaCancer pipeline completed successfully.")


if __name__ == "__main__":
    main()
