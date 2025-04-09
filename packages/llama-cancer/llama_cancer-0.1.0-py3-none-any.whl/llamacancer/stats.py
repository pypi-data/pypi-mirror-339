# llamacancer/stats.py
import logging
from typing import Any, Dict, List, Optional

import numpy as np
import pandas as pd
import statsmodels.api as sm
from lifelines import CoxPHFitter
from lifelines.statistics import logrank_test
from scipy import stats as sp_stats
from statsmodels.stats.multitest import multipletests


def run_logrank_test(
    durations: pd.Series, events: pd.Series, groups: pd.Series
) -> Optional[Dict[str, float]]:
    """Performs a log-rank test between groups."""
    combined = pd.concat([durations, events, groups], axis=1).dropna()
    if len(combined) < 2 or combined[groups.name].nunique() < 2:
        logging.warning("Insufficient data/groups for logrank test.")
        return None
    durations_clean = combined[durations.name]
    events_clean = combined[events.name].astype(int)
    groups_clean = combined[groups.name]
    group_labels = sorted(groups_clean.unique())

    try:
        if len(group_labels) == 2:
            results = logrank_test(
                durations_clean[groups_clean == group_labels[0]],
                durations_clean[groups_clean == group_labels[1]],
                event_observed_A=events_clean[groups_clean == group_labels[0]],
                event_observed_B=events_clean[groups_clean == group_labels[1]],
            )
            return {
                "logrank_test_statistic": results.test_statistic,
                "p_value": results.p_value,
            }
        elif len(group_labels) > 2:
            results = logrank_test(
                event_durations=durations_clean,
                event_observed=events_clean,
                groups=groups_clean,
            )
            return {
                "logrank_test_statistic": results.test_statistic,
                "p_value": results.p_value,
            }
        else:
            return None
    except Exception as e:
        logging.error(f"Logrank test failed: {e}", exc_info=True)
        return None


def fit_coxph_model(
    df: pd.DataFrame,
    duration_col: str,
    event_col: str,
    covariates: List[str],
    reference_group: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Fits a Cox Proportional Hazards model.

    Args:
        df: DataFrame with survival data
        duration_col: Column name with time to event
        event_col: Column name with event indicator (1=event, 0=censored)
        covariates: List of covariate column names
        reference_group: For categorical covariates, the reference level (default=None)

    Returns:
        Dictionary with model results
    """
    required_cols = [duration_col, event_col] + covariates
    if not all(c in df.columns for c in required_cols):
        missing = [c for c in required_cols if c not in df.columns]
        logging.error(f"Missing columns for CoxPH model: {missing}")
        return None

    df_clean = df[required_cols].dropna()
    if len(df_clean) < len(covariates) + 2:
        logging.warning(f"Insufficient data for CoxPH model: {len(df_clean)} rows.")
        return None

    try:
        # Create formula with reference categories if specified
        formula = ""
        for i, covariate in enumerate(covariates):
            if i > 0:
                formula += " + "

            # Handle categorical variables with reference group
            if reference_group is not None and df_clean[covariate].dtype == "object":
                formula += f"C({covariate}, Treatment(reference='{reference_group}'))"
            else:
                formula += covariate

        cph = CoxPHFitter()
        df_clean[event_col] = df_clean[event_col].astype(int)
        cph.fit(df_clean, duration_col=duration_col, event_col=event_col, formula=formula)

        # Extract model summary
        summary = cph.summary

        # Create a more user-friendly results dict
        results = {}

        # Get the first row for single-covariate case
        if len(summary) > 0:
            first_row = summary.iloc[0]
            results["hazard_ratio"] = float(first_row["exp(coef)"])
            results["lower_ci"] = float(first_row["exp(coef) lower 95%"])
            results["upper_ci"] = float(first_row["exp(coef) upper 95%"])
            results["p_value"] = float(first_row["p"])
            results["concordance_index"] = float(cph.concordance_index_)
            results["log_likelihood"] = float(cph.log_likelihood_)

        return results
    except Exception as e:
        logging.error(f"CoxPH model fitting failed: {e}", exc_info=True)
        return None


def fisher_exact_test(table: List[List[int]]) -> Optional[Dict[str, float]]:
    """
    Performs Fisher's exact test on a 2x2 contingency table.

    Args:
        table: 2x2 contingency table as a list of lists

    Returns:
        Dictionary with odds ratio and p-value
    """
    try:
        # Validate input
        if len(table) != 2 or len(table[0]) != 2 or len(table[1]) != 2:
            logging.error(f"Fisher's exact test requires a 2x2 table, got: {table}")
            return None

        # Convert to numpy array
        table_arr = np.array(table)

        # If any cell has 0, add a small correction
        if np.any(table_arr == 0):
            logging.warning(
                "Zero cells found in contingency table. Adding 0.5 correction to all cells."
            )
            table_arr = table_arr + 0.5

        # Run the test
        odds_ratio, p_value = sp_stats.fisher_exact(table_arr)

        return {"odds_ratio": float(odds_ratio), "p_value": float(p_value)}
    except Exception as e:
        logging.error(f"Fisher's exact test failed: {e}", exc_info=True)
        return None


def run_logistic_regression(
    df: pd.DataFrame,
    outcome_col: str,
    covariates: List[str],
    reference_group: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Fits a logistic regression model.

    Args:
        df: DataFrame with outcome and predictors
        outcome_col: Column name with binary outcome (1=positive, 0=negative)
        covariates: List of covariate column names
        reference_group: For categorical covariates, the reference level (default=None)

    Returns:
        Dictionary with model results
    """
    required_cols = [outcome_col] + covariates
    if not all(c in df.columns for c in required_cols):
        missing = [c for c in required_cols if c not in df.columns]
        logging.error(f"Missing columns for logistic regression: {missing}")
        return None

    df_clean = df[required_cols].dropna()
    if len(df_clean) < len(covariates) + 5:  # Need more samples for logistic than Cox
        logging.warning(f"Insufficient data for logistic regression: {len(df_clean)} rows.")
        return None

    try:
        # Convert outcome to binary
        y = df_clean[outcome_col].astype(int)

        # Add constant for intercept
        X = df_clean[covariates].copy()

        # Handle categorical variables with reference group
        if reference_group is not None:
            for covariate in covariates:
                if X[covariate].dtype == "object":
                    # Create dummy variables with specified reference
                    dummies = pd.get_dummies(X[covariate], prefix=covariate, drop_first=False)
                    # Drop the reference group column
                    ref_col = f"{covariate}_{reference_group}"
                    if ref_col in dummies.columns:
                        dummies = dummies.drop(columns=[ref_col])
                    # Drop original column and add dummies
                    X = X.drop(columns=[covariate])
                    X = pd.concat([X, dummies], axis=1)

        # Add constant
        X = sm.add_constant(X)

        # Fit the model
        logit_model = sm.Logit(y, X)
        result = logit_model.fit(disp=0)  # Suppress convergence messages

        # Extract results
        coef = result.params[1]  # First covariate coefficient (after constant)
        odds_ratio = np.exp(coef)
        ci = result.conf_int()
        lower_ci = np.exp(ci.iloc[1, 0])  # First covariate lower CI
        upper_ci = np.exp(ci.iloc[1, 1])  # First covariate upper CI
        p_value = result.pvalues[1]  # First covariate p-value

        return {
            "coefficient": float(coef),
            "odds_ratio": float(odds_ratio),
            "lower_ci": float(lower_ci),
            "upper_ci": float(upper_ci),
            "p_value": float(p_value),
            "aic": float(result.aic),
            "log_likelihood": float(result.llf),
        }
    except Exception as e:
        logging.error(f"Logistic regression failed: {e}", exc_info=True)
        return None


def run_group_comparison(
    data: pd.DataFrame, value_col: str, group_col: str, config: object
) -> Optional[Dict[str, float]]:
    """Runs a group comparison test for a given variable."""
    if value_col not in data.columns or group_col not in data.columns:
        logging.error(f"Missing column(s) for group comparison: {value_col}, {group_col}")
        return None
    is_continuous = pd.api.types.is_numeric_dtype(data[value_col]) and data[value_col].nunique() > 5
    stat_result = None
    if is_continuous:
        method = config.group_comparison_stat_continuous
        logging.info(f"Comparing continuous variable '{value_col}' by '{group_col}' using {method}")
        groups = data[group_col].dropna().unique()
        if len(groups) != 2:
            logging.warning("T-test/Mann-Whitney U requires exactly 2 groups.")
            return None
        group1 = data[value_col][data[group_col] == groups[0]].dropna()
        group2 = data[value_col][data[group_col] == groups[1]].dropna()
        if method.lower() == "ttest":
            stat, p = sp_stats.ttest_ind(group1, group2, equal_var=False, nan_policy="omit")
            stat_result = {"t_stat": stat, "p_value": p}
        elif method.lower() == "mannwhitneyu":
            try:
                stat, p = sp_stats.mannwhitneyu(
                    group1, group2, alternative="two-sided", nan_policy="omit"
                )
                stat_result = {"u_stat": stat, "p_value": p}
            except ValueError as e:
                logging.warning(f"Mann-Whitney U test failed: {e}")
                stat_result = {"u_stat": float("nan"), "p_value": 1.0}
        else:
            logging.warning(f"Unsupported method {method} for continuous comparison.")
            return None
    else:
        method = config.group_comparison_stat_categorical
        logging.info(
            f"Comparing categorical variable '{value_col}' by '{group_col}' using {method}"
        )
        try:
            contingency_table = pd.crosstab(data[value_col], data[group_col])
            if contingency_table.shape[0] < 2 or contingency_table.shape[1] < 2:
                logging.warning("Contingency table too small for test.")
                return None
            if method.lower() == "chisquare":
                chi2, p, dof, expected = sp_stats.chi2_contingency(contingency_table)
                stat_result = {"chi2_stat": chi2, "p_value": p, "dof": dof}
            elif method.lower() == "fisherexact":
                oddsr, p = sp_stats.fisher_exact(contingency_table)
                stat_result = {"odds_ratio": oddsr, "p_value": p}
            else:
                logging.warning(f"Unsupported categorical method {method}.")
                return None
        except Exception as e:
            logging.error(f"Categorical test failed: {e}", exc_info=True)
            return None

    return {k: float(v) if pd.notna(v) else None for k, v in stat_result.items()}


def run_correlation_analysis(
    data: pd.DataFrame, var1_col: str, var2_col: str, config: object
) -> Optional[Dict[str, float]]:
    """Calculates correlation between two variables."""
    method = config.correlation_method.lower()
    if var1_col not in data.columns or var2_col not in data.columns:
        logging.error(f"Missing columns for correlation: {var1_col}, {var2_col}")
        return None
    valid_data = data[[var1_col, var2_col]].dropna()
    if len(valid_data) < 3:
        logging.warning("Too few data points for correlation.")
        return None
    try:
        if method == "pearson":
            corr, p_val = sp_stats.pearsonr(valid_data[var1_col], valid_data[var2_col])
        elif method == "spearman":
            corr, p_val = sp_stats.spearmanr(valid_data[var1_col], valid_data[var2_col])
        else:
            logging.warning(f"Unsupported correlation method: {method}")
            return None
        return {"correlation": float(corr), "p_value": float(p_val)}
    except Exception as e:
        logging.error(f"Correlation analysis failed: {e}", exc_info=True)
        return None


def adjust_p_values(p_values, method: str = "fdr_bh") -> np.ndarray:
    """Adjusts p-values for multiple testing."""
    p_values_array = np.asarray(p_values)
    nan_mask = np.isnan(p_values_array)
    p_vals_to_adjust = p_values_array[~nan_mask]
    if len(p_vals_to_adjust) == 0:
        return p_values_array
    _, pvals_adjusted, _, _ = multipletests(p_vals_to_adjust, alpha=0.05, method=method)
    adjusted_array = np.full_like(p_values_array, np.nan, dtype=float)
    adjusted_array[~nan_mask] = pvals_adjusted
    return adjusted_array
