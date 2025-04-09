# llamacancer/vis.py
import logging
import os
from typing import Any, Dict, List, Optional, Union

import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
import numpy as np
import pandas as pd
import seaborn as sns

from .utils import safe_log_p_value

try:
    from lifelines import KaplanMeierFitter
    from lifelines.plotting import add_at_risk_counts

    lifelines_imported = True
except ImportError:
    KaplanMeierFitter = None
    add_at_risk_counts = None
    lifelines_imported = False


def save_plot(fig, filename: str, results_dir: str):
    """Saves the figure to the specified directory."""
    if not os.path.exists(results_dir):
        os.makedirs(results_dir, exist_ok=True)

    # Ensure we don't duplicate the results directory in the path
    if filename.startswith(results_dir):
        filepath = filename
    else:
        filepath = os.path.join(results_dir, filename)

    fig.savefig(filepath, dpi=150)
    plt.close(fig)
    logging.info(f"Plot saved: {filepath}")


def plot_kaplan_meier(
    df: pd.DataFrame,
    duration_col: str,
    event_col: str,
    group_col: Optional[str] = None,
    group_labels: Optional[Dict[Any, Any]] = None,
    title: Optional[str] = None,
    config: Any = None,
    results_dir: Optional[str] = None,
    filename: Optional[str] = None,
    test_results: Optional[Dict] = None,
):
    """Plots Kaplan–Meier survival curves."""
    if not lifelines_imported:
        logging.error("Lifelines not installed. Install via 'pip install lifelines'.")
        return
    if duration_col not in df.columns or event_col not in df.columns:
        logging.error("Missing duration or event column for KM plot.")
        return
    res_dir = results_dir or config.get("results_dir", "results")
    style = config.get("plot_style", "seaborn-v0_8-whitegrid")
    palette = config.get("plot_palette", "viridis")
    show_ci = config.get("km_plot_conf_int", True)
    time_unit = (
        config.endpoints.get(config.primary_endpoint, {}).get("unit", "Time Units")
        if config
        else "Time Units"
    )
    mplstyle.use(style)
    fig, ax = plt.subplots(figsize=(8, 6))
    kmf = KaplanMeierFitter()
    if group_col:
        groups = sorted(df[group_col].dropna().unique())
        cmap = plt.get_cmap(palette, len(groups))
        for i, group_val in enumerate(groups):
            mask = df[group_col] == group_val
            if mask.sum() == 0:
                continue
            label = group_labels.get(group_val, group_val) if group_labels else group_val
            kmf.fit(df.loc[mask, duration_col], df.loc[mask, event_col], label=str(label))
            kmf.plot_survival_function(ax=ax, ci_show=show_ci, color=cmap(i))
        if test_results and "p_value" in test_results:
            ax.text(
                0.05,
                0.05,
                f"Log-Rank p = {test_results['p_value']:.3g}",
                transform=ax.transAxes,
                fontsize=10,
            )
    else:
        kmf.fit(df[duration_col], df[event_col], label="All Subjects")
        kmf.plot_survival_function(ax=ax, ci_show=show_ci)
    if config.get("km_plot_at_risk", True):
        try:
            add_at_risk_counts(kmf, ax=ax, rows_to_show=["At risk"])
        except Exception as e:
            logging.warning(f"Could not add 'at risk' table: {e}")
    ax.set_xlabel(f"Time ({time_unit})")
    ax.set_ylabel("Survival Probability")
    ax.set_ylim(0, 1.05)
    ax.legend(loc="best")
    plot_title = title or f"Kaplan-Meier Estimate ({duration_col})"
    if group_col:
        plot_title += f" by {group_col}"
    ax.set_title(plot_title)
    ax.grid(True, linestyle=":", alpha=0.6)
    fig.tight_layout()
    fname = filename or f"kaplan_meier_{duration_col}"
    if group_col:
        fname += f"_by_{group_col}"
    fname += f".{config.plot_format}" if config else ".png"
    save_plot(fig, fname, res_dir)
    return True


def plot_volcano(
    x_values: Union[pd.DataFrame, List[float], np.ndarray] = None,
    p_values: Optional[List[float]] = None,
    labels: Optional[List[str]] = None,
    results_df: Optional[pd.DataFrame] = None,
    fdr_col: Optional[str] = None,
    sig_threshold: float = 0.05,
    fc_threshold: float = 0.0,
    label_col: Optional[str] = None,
    n_labels: int = 10,
    x_label: str = "Log2 Fold Change",
    y_label: str = "-Log10 P-value",
    title: Optional[str] = None,
    config: Any = None,
    results_dir: Optional[str] = None,
    filename: Optional[str] = "volcano_plot.png",
):
    """
    Creates a volcano plot from association results.

    Can be called in two ways:
    1. Directly with x_values (e.g., hazard ratios), p_values, and labels
    2. With a results_df containing 'log2FoldChange' and 'p_value' columns

    Args:
        x_values: List of x-values (e.g., hazard ratios or log2 fold changes)
        p_values: List of p-values corresponding to x_values
        labels: Optional list of labels for points
        results_df: DataFrame with results (alternative to direct values)
        fdr_col: Column name with adjusted p-values
        sig_threshold: Significance threshold for p-values
        fc_threshold: Fold change threshold for significance
        label_col: Column with labels (when using results_df)
        n_labels: Number of top significant points to label
        x_label: Label for x-axis
        y_label: Label for y-axis
        title: Plot title
        config: Configuration object
        results_dir: Directory to save plot
        filename: Filename for output plot

    Returns:
        True if successful, None otherwise
    """
    conf = config or {}
    res_dir = results_dir or conf.get("results_dir", "results")
    style = conf.get("plot_style", "seaborn-v0_8-whitegrid")
    plt_dpi = conf.get("plot_dpi", 150)
    mplstyle.use(style)

    # Create the plot dataframe
    if results_df is not None and not results_df.empty:
        # Method 1: Using a DataFrame
        if "log2FoldChange" not in results_df.columns or "p_value" not in results_df.columns:
            logging.error("Volcano plot requires 'log2FoldChange' and 'p_value' columns.")
            return None

        plot_df = results_df.copy()
        plot_df["-log10(p)"] = plot_df["p_value"].apply(safe_log_p_value)
        x_col = "log2FoldChange"

    elif x_values is not None and p_values is not None:
        # Method 2: Using direct lists/arrays
        if len(x_values) != len(p_values):
            logging.error(f"Length mismatch: x_values={len(x_values)}, p_values={len(p_values)}")
            return None

        plot_df = pd.DataFrame(
            {
                "x_value": x_values,
                "p_value": p_values,
                "-log10(p)": [safe_log_p_value(p) for p in p_values],
            }
        )

        if labels is not None and len(labels) == len(x_values):
            plot_df["label"] = labels

        x_col = "x_value"

    else:
        logging.error("Either results_df or both x_values and p_values must be provided")
        return None

    # Check for valid p-values
    if plot_df["-log10(p)"].isna().all():
        logging.warning("No valid p-values for volcano plot.")
        return None

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))

    # Determine significance
    p_col = fdr_col if (fdr_col and fdr_col in plot_df.columns) else "p_value"
    neglog10_p_thresh = safe_log_p_value(sig_threshold) or 1.3

    plot_df["Significance"] = "Not Significant"
    mask_up = (plot_df[p_col] < sig_threshold) & (plot_df[x_col] > fc_threshold)
    plot_df.loc[mask_up, "Significance"] = f"Significant ({x_label} > {fc_threshold:.2f})"

    mask_down = (plot_df[p_col] < sig_threshold) & (plot_df[x_col] < -fc_threshold)
    plot_df.loc[mask_down, "Significance"] = f"Significant ({x_label} < {-fc_threshold:.2f})"

    # Plot points
    sns.scatterplot(
        data=plot_df,
        x=x_col,
        y="-log10(p)",
        hue="Significance",
        palette={
            "Not Significant": "grey",
            f"Significant ({x_label} > {fc_threshold:.2f})": "red",
            f"Significant ({x_label} < {-fc_threshold:.2f})": "blue",
        },
        alpha=0.7,
        s=80,  # Point size
        ax=ax,
    )

    # Add threshold lines
    ax.axhline(neglog10_p_thresh, color="grey", linestyle="--", alpha=0.7)
    if fc_threshold > 0:
        ax.axvline(fc_threshold, color="grey", linestyle="--", alpha=0.7)
        ax.axvline(-fc_threshold, color="grey", linestyle="--", alpha=0.7)

    # Add labels to significant points
    label_col_to_use = None
    if labels is not None and "label" in plot_df.columns:
        label_col_to_use = "label"
    elif label_col and label_col in plot_df.columns:
        label_col_to_use = label_col

    if label_col_to_use and n_labels > 0:
        sig_df = (
            plot_df[plot_df["Significance"] != "Not Significant"]
            .sort_values("-log10(p)", ascending=False)
            .head(n_labels)
        )
        texts = []
        try:
            from adjustText import adjust_text

            for _, row in sig_df.iterrows():
                texts.append(
                    ax.text(
                        row[x_col],
                        row["-log10(p)"],
                        str(row[label_col_to_use]),
                        fontsize=9,
                    )
                )
            adjust_text(texts, arrowprops=dict(arrowstyle="-", color="black", lw=0.5), ax=ax)
        except ImportError:
            logging.warning("adjustText not installed; labels may overlap.")
            for _, row in sig_df.iterrows():
                ax.text(row[x_col], row["-log10(p)"], str(row[label_col_to_use]), fontsize=9)
        except Exception as e_adj:
            logging.warning(f"Error adding labels: {e_adj}")

    # Finalize plot
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title(title or "Volcano Plot")
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(title="Significance", bbox_to_anchor=(1.05, 1), loc="upper left")

    fig.tight_layout()
    save_plot(fig, filename, res_dir)
    return True


def plot_forest(
    hr_values: List[float],
    ci_lowers: List[float],
    ci_uppers: List[float],
    labels: List[str],
    title: Optional[str] = "Hazard Ratios",
    sort_by_hr: bool = False,
    config: Any = None,
    results_dir: Optional[str] = None,
    filename: Optional[str] = "forest_plot.png",
):
    """
    Create a forest plot for hazard ratios or odds ratios with confidence intervals.

    Args:
        hr_values: List of hazard ratio or odds ratio values
        ci_lowers: List of lower confidence interval bounds
        ci_uppers: List of upper confidence interval bounds
        labels: List of labels for each value (biomarker names)
        title: Plot title
        sort_by_hr: Whether to sort by hazard ratio value (default: False)
        config: Configuration object
        results_dir: Directory to save plot
        filename: Filename for output plot

    Returns:
        True if successful, None otherwise
    """
    # Check if we have any valid data
    if len(hr_values) == 0:
        logging.warning("No data provided for forest plot.")
        return None

    if (
        len(hr_values) != len(ci_lowers)
        or len(hr_values) != len(ci_uppers)
        or len(hr_values) != len(labels)
    ):
        logging.error(
            f"Length mismatch: values={len(hr_values)}, CIs={len(ci_lowers)}/{len(ci_uppers)}, labels={len(labels)}"
        )
        return None

    conf = config or {}
    res_dir = results_dir or conf.get("results_dir", "results")
    style = conf.get("plot_style", "seaborn-v0_8-whitegrid")
    plt_dpi = conf.get("plot_dpi", 150)
    mplstyle.use(style)

    # Create DataFrame
    df = pd.DataFrame(
        {
            "Label": labels,
            "HR": hr_values,
            "CI_lower": ci_lowers,
            "CI_upper": ci_uppers,
            "Error_low": [hr - low for hr, low in zip(hr_values, ci_lowers)],
            "Error_high": [high - hr for hr, high in zip(hr_values, ci_uppers)],
        }
    )

    # Handle possible NaN/Inf values
    df = df.replace([np.inf, -np.inf], np.nan).dropna()

    if df.empty:
        logging.warning("No valid data after cleaning NaN/Inf values for forest plot.")
        return None

    # Sort if requested
    if sort_by_hr:
        df = df.sort_values("HR", ascending=False)

    # Create figure
    fig, ax = plt.subplots(figsize=(10, max(6, 0.5 * len(df))))

    # Plot
    y_pos = range(len(df))
    ax.errorbar(
        x=df["HR"],
        y=y_pos,
        xerr=[df["Error_low"], df["Error_high"]],
        fmt="o",
        capsize=5,
        capthick=1.5,
        elinewidth=1.5,
        markersize=8,
        color="#1f77b4",
    )

    # Add reference line
    ax.axvline(x=1, color="red", linestyle="--", alpha=0.7, label="No Effect")

    # Add labels and formatting
    ax.set_yticks(y_pos)
    ax.set_yticklabels(df["Label"])
    ax.set_xlabel("Hazard Ratio (95% CI)")
    ax.set_title(title)
    ax.grid(True, linestyle=":", alpha=0.6, axis="x")

    # Display HR values and CIs
    for i, row in enumerate(df.itertuples()):
        ax.text(
            row.HR + 0.1,
            i,
            f"{row.HR:.2f} ({row.CI_lower:.2f}-{row.CI_upper:.2f})",
            va="center",
        )

    # Adjust x-axis range to fit text
    if len(df) > 0:
        x_max = max(df["CI_upper"].max() * 1.5, 2.0)  # Ensure minimum range
        x_min = max(0, df["CI_lower"].min() * 0.8)  # Ensure non-negative min
        ax.set_xlim(x_min, x_max)

    fig.tight_layout()
    save_plot(fig, filename, res_dir)
    return True
