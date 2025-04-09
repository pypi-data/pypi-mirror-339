# llamacancer/analysis.py
import logging
import os
from typing import Any, Dict, Optional

import matplotlib.pyplot as plt
import pandas as pd

from .endpoints import get_endpoint_data
from .stats import (
    fisher_exact_test,
    fit_coxph_model,
    run_logistic_regression,
    run_logrank_test,
)
from .vis import plot_forest, plot_kaplan_meier, plot_volcano


def run_biomarker_associations(df: pd.DataFrame, config) -> Dict[str, Any]:
    """
    A high-level function to perform biomarker associations with endpoints.
    This function integrates data filtering, statistical testing, and visualization.

    Args:
        df: Merged dataframe containing clinical and biomarker data
        config: Configuration object with analysis settings

    Returns:
        Dictionary containing results of all biomarker association analyses
    """
    logging.info("Running biomarker association analyses...")
    results = {"survival": {}, "response": {}, "summary": {}}

    # Ensure results directory exists
    os.makedirs(config.results_dir, exist_ok=True)

    # Get primary endpoint data
    primary_endpoint = config.primary_endpoint

    # Track statistics for all biomarkers for summary plots
    hr_values = []
    p_values = []
    biomarker_names = []
    ci_lowers = []
    ci_uppers = []

    # Process each biomarker
    for biomarker in config.biomarkers_to_analyze:
        logging.info(f"Analyzing biomarker: {biomarker}")

        # Skip if biomarker column doesn't exist
        if biomarker not in df.columns:
            logging.warning(f"Biomarker '{biomarker}' not found in dataset. Skipping.")
            continue

        # Create high/low groups for the biomarker
        df_with_groups = _dichotomize_biomarker(df, biomarker, config)
        if df_with_groups is None:
            continue

        group_col = f"{biomarker}_group"

        # Survival analysis
        if primary_endpoint in config.endpoints and hasattr(
            config.endpoints[primary_endpoint], "time_col"
        ):
            survival_results = _analyze_survival_by_biomarker(
                df_with_groups, biomarker, group_col, primary_endpoint, config
            )

            if survival_results:
                results["survival"][biomarker] = survival_results

                # Track for summary plots
                if "cox_results" in survival_results:
                    hr_values.append(survival_results["cox_results"]["hazard_ratio"])
                    p_values.append(survival_results["cox_results"]["p_value"])
                    biomarker_names.append(biomarker)
                    ci_lowers.append(survival_results["cox_results"]["lower_ci"])
                    ci_uppers.append(survival_results["cox_results"]["upper_ci"])

        # Response analysis
        if "response" in config.endpoints and hasattr(config.endpoints.response, "response_col"):
            response_results = _analyze_response_by_biomarker(
                df_with_groups, biomarker, group_col, config
            )

            if response_results:
                results["response"][biomarker] = response_results

    # Create summary plots
    if len(hr_values) > 0:
        # Create forest plot of hazard ratios
        plot_forest(
            hr_values=hr_values,
            ci_lowers=ci_lowers,
            ci_uppers=ci_uppers,
            labels=biomarker_names,
            title=f"Hazard Ratios for {primary_endpoint}",
            filename=os.path.join(config.results_dir, "biomarker_forest_plot.png"),
            config=config,
        )

        # Create volcano plot
        plot_volcano(
            x_values=hr_values,
            p_values=p_values,
            labels=biomarker_names,
            x_label="Hazard Ratio",
            title=f"Biomarker Associations with {primary_endpoint}",
            filename=os.path.join(config.results_dir, "biomarker_volcano_plot.png"),
            config=config,
        )

    results["summary"] = {
        "num_biomarkers_analyzed": len(results["survival"]),
        "significant_biomarkers": [
            b
            for b, v in results["survival"].items()
            if "cox_results" in v and v["cox_results"]["p_value"] < config.alpha_threshold
        ],
    }

    logging.info(
        f"Analysis complete. Analyzed {results['summary']['num_biomarkers_analyzed']} biomarkers."
    )
    return results


def _dichotomize_biomarker(df: pd.DataFrame, biomarker: str, config) -> Optional[pd.DataFrame]:
    """
    Create high/low groups for a biomarker based on config settings.

    Args:
        df: Input dataframe
        biomarker: Name of biomarker column
        config: Configuration object

    Returns:
        DataFrame with added group column, or None if error
    """
    df_copy = df.copy()
    group_col = f"{biomarker}_group"

    # Handle missing data
    if df_copy[biomarker].isna().all():
        logging.warning(f"Biomarker '{biomarker}' has all missing values. Skipping.")
        return None

    # For categorical biomarkers
    if biomarker in config.biomarker_positive_categories:
        positive_value = config.biomarker_positive_categories[biomarker]
        df_copy[group_col] = df_copy[biomarker].apply(
            lambda x: "High" if x == positive_value else "Low"
        )
        logging.info(f"Dichotomized '{biomarker}' based on positive category: {positive_value}")

    # For continuous biomarkers with cutoffs
    elif biomarker in config.biomarker_cutoffs:
        cutoff_value = config.biomarker_cutoffs[biomarker]

        if cutoff_value == "median":
            cutoff = df_copy[biomarker].median()
            df_copy[group_col] = df_copy[biomarker].apply(
                lambda x: "High" if x >= cutoff else "Low"
            )
            logging.info(f"Dichotomized '{biomarker}' at median: {cutoff:.3f}")

        elif cutoff_value == "quartile":
            q1 = df_copy[biomarker].quantile(0.25)
            q3 = df_copy[biomarker].quantile(0.75)
            df_copy[group_col] = df_copy[biomarker].apply(
                lambda x: "High" if x >= q3 else ("Low" if x <= q1 else "Medium")
            )
            # Remove medium values for binary analysis
            df_copy = df_copy[df_copy[group_col] != "Medium"]
            logging.info(f"Dichotomized '{biomarker}' at quartiles: Q1={q1:.3f}, Q3={q3:.3f}")

        elif isinstance(cutoff_value, (int, float)):
            df_copy[group_col] = df_copy[biomarker].apply(
                lambda x: "High" if x >= cutoff_value else "Low"
            )
            logging.info(f"Dichotomized '{biomarker}' at fixed value: {cutoff_value}")

        else:
            logging.warning(f"Unrecognized cutoff type for '{biomarker}': {cutoff_value}")
            return None

    # Default to median
    else:
        cutoff = df_copy[biomarker].median()
        df_copy[group_col] = df_copy[biomarker].apply(lambda x: "High" if x >= cutoff else "Low")
        logging.info(f"Dichotomized '{biomarker}' at median: {cutoff:.3f}")

    # Check if we have both groups
    value_counts = df_copy[group_col].value_counts()
    if len(value_counts) < 2:
        logging.warning(
            f"Biomarker '{biomarker}' does not have both High and Low groups after dichotomization."
        )
        return None

    # Log the distribution
    logging.info(f"Group distribution for '{biomarker}': {dict(value_counts)}")

    return df_copy


def _analyze_survival_by_biomarker(
    df: pd.DataFrame, biomarker: str, group_col: str, endpoint: str, config
) -> Dict[str, Any]:
    """
    Perform survival analysis for a biomarker.

    Args:
        df: DataFrame with biomarker groups
        biomarker: Original biomarker name
        group_col: Column with High/Low groups
        endpoint: Endpoint name from config
        config: Configuration object

    Returns:
        Dictionary with survival analysis results
    """
    results = {}

    # Get endpoint data
    duration, event = get_endpoint_data(df, endpoint, config)
    if duration is None or event is None:
        logging.warning(
            f"Could not extract endpoint data for '{endpoint}'. Skipping survival analysis."
        )
        return results

    # Run log-rank test between biomarker groups
    logrank_results = run_logrank_test(duration, event, df[group_col])
    if logrank_results:
        results["logrank_results"] = logrank_results

    # Run Cox PH model
    cox_results = fit_coxph_model(
        df,
        duration_col=config.endpoints[endpoint].time_col,
        event_col=config.endpoints[endpoint].status_col,
        covariates=[group_col],
        reference_group="Low",
    )
    if cox_results:
        results["cox_results"] = cox_results

    # Generate Kaplan-Meier plot
    plot_file = os.path.join(config.results_dir, f"km_{endpoint}_{biomarker}.{config.plot_format}")

    km_plot = plot_kaplan_meier(
        df=df,
        duration_col=config.endpoints[endpoint].time_col,
        event_col=config.endpoints[endpoint].status_col,
        group_col=group_col,
        title=f"{endpoint} by {biomarker}",
        filename=plot_file,
        test_results=logrank_results,
        config=config,
    )

    if km_plot:
        results["plots"] = {"km_plot": plot_file}

    return results


def _analyze_response_by_biomarker(
    df: pd.DataFrame, biomarker: str, group_col: str, config
) -> Dict[str, Any]:
    """
    Analyze association between biomarker and response.

    Args:
        df: DataFrame with biomarker groups
        biomarker: Original biomarker name
        group_col: Column with High/Low groups
        config: Configuration object

    Returns:
        Dictionary with response analysis results
    """
    results = {}

    # Get response data
    response_col = config.endpoints.response.response_col
    if response_col not in df.columns:
        logging.warning(f"Response column '{response_col}' not found in dataset.")
        return results

    # Create binary response (responder/non-responder)
    df_with_response = df.copy()
    positive_values = config.endpoints.response.positive_values
    df_with_response["responder"] = df_with_response[response_col].apply(
        lambda x: 1 if x in positive_values else 0
    )

    # Run Fisher's exact test
    resp_high = df_with_response[
        (df_with_response[group_col] == "High") & (df_with_response["responder"] == 1)
    ].shape[0]
    resp_low = df_with_response[
        (df_with_response[group_col] == "Low") & (df_with_response["responder"] == 1)
    ].shape[0]
    nonresp_high = df_with_response[
        (df_with_response[group_col] == "High") & (df_with_response["responder"] == 0)
    ].shape[0]
    nonresp_low = df_with_response[
        (df_with_response[group_col] == "Low") & (df_with_response["responder"] == 0)
    ].shape[0]

    table = [[resp_high, resp_low], [nonresp_high, nonresp_low]]
    fisher_results = fisher_exact_test(table)
    if fisher_results:
        results["fisher_results"] = fisher_results

    # Run logistic regression
    logreg_results = run_logistic_regression(
        df_with_response,
        outcome_col="responder",
        covariates=[group_col],
        reference_group="Low",
    )
    if logreg_results:
        results["logreg_results"] = logreg_results

    # Create bar plot of response rates by biomarker group
    try:
        plt.figure(figsize=(8, 6))
        grouped = df_with_response.groupby(group_col)["responder"].mean() * 100
        grouped.plot(kind="bar", color=["#3498db", "#e74c3c"])
        plt.ylabel("Response Rate (%)")
        plt.title(f"Response Rate by {biomarker} Group")
        plt.ylim(0, 100)

        # Add p-value annotation
        if "fisher_results" in results:
            pval = results["fisher_results"]["p_value"]
            plt.annotate(
                f"p = {pval:.3f}",
                xy=(0.5, 0.9),
                xycoords="axes fraction",
                ha="center",
                fontsize=12,
            )

        plot_file = os.path.join(config.results_dir, f"response_{biomarker}.{config.plot_format}")
        plt.tight_layout()
        plt.savefig(plot_file, dpi=config.plot_dpi)
        plt.close()

        results["plots"] = {"response_plot": plot_file}
    except Exception as e:
        logging.error(f"Error creating response plot for {biomarker}: {e}")

    return results
