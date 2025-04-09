# llamacancer/utils.py
import logging
import os
import warnings
from typing import Any, Optional

import numpy as np
import pandas as pd


def setup_logging(level="INFO", log_file: Optional[str] = None):
    """Configures basic logging."""
    log_level = getattr(logging, level.upper(), logging.INFO)
    log_format = "%(asctime)s - %(levelname)s - %(module)s - %(message)s"
    handlers = [logging.StreamHandler()]
    if log_file:
        try:
            log_dir = os.path.dirname(log_file)
            if log_dir:
                os.makedirs(log_dir, exist_ok=True)
            handlers.append(logging.FileHandler(log_file, mode="a"))
        except Exception as e:
            print(f"Warning: Could not create log file handler for {log_file}. Error: {e}")
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    logging.basicConfig(level=log_level, format=log_format, handlers=handlers)
    logging.info(f"Logging configured at level: {level}")


def ensure_numeric(series: pd.Series, column_name: str, errors: str = "coerce") -> pd.Series:
    """Converts a pandas Series to numeric with warning on failure."""
    if pd.api.types.is_numeric_dtype(series):
        return series
    original_dtype = series.dtype
    numeric_series = pd.to_numeric(series, errors=errors)
    num_nan_generated = numeric_series.isna().sum() - series.isna().sum()
    if num_nan_generated > 0:
        warnings.warn(
            f"Column '{column_name}': {num_nan_generated} non-numeric values (original dtype: {original_dtype}) coerced to NaN.",
            UserWarning,
        )
    return numeric_series


def dichotomize_biomarker(
    series: pd.Series,
    cutoff_method: Any,  # e.g., 'median', 'quartile' or a specific threshold
    positive_category_name: str = "High",
    negative_category_name: str = "Low",
) -> Optional[pd.Series]:
    """Dichotomizes a continuous biomarker series based on a cutoff."""
    if not pd.api.types.is_numeric_dtype(series):
        logging.warning(f"Cannot dichotomize non-numeric series: {series.name}")
        return None
    if series.isna().all():
        logging.warning(f"Series {series.name} has all NaN values.")
        return None

    series_clean = series.dropna()
    cutoff_val = None
    if isinstance(cutoff_method, (int, float)):
        cutoff_val = cutoff_method
        logging.info(f"Dichotomizing '{series.name}' using threshold: {cutoff_val}")
    elif isinstance(cutoff_method, str):
        if cutoff_method.lower() == "median":
            cutoff_val = series_clean.median()
            logging.info(f"Dichotomizing '{series.name}' using median: {cutoff_val:.3f}")
        elif cutoff_method.lower() == "mean":
            cutoff_val = series_clean.mean()
            logging.info(f"Dichotomizing '{series.name}' using mean: {cutoff_val:.3f}")
        elif cutoff_method.lower() == "quartile":
            q1 = series_clean.quantile(0.25)
            q3 = series_clean.quantile(0.75)
            logging.info(f"Categorizing '{series.name}' using quartiles: Q1={q1:.3f}, Q3={q3:.3f}")
            groups = pd.cut(
                series,
                bins=[-np.inf, q1, q3, np.inf],
                labels=["Low", "Mid", "High"],
                right=True,
            )
            return groups.rename(f"{series.name}_QuartileGroup")
        else:
            logging.warning(f"Unsupported cutoff method '{cutoff_method}' for {series.name}")
            return None
    else:
        logging.warning(f"Invalid cutoff method type: {type(cutoff_method)} for {series.name}")
        return None

    binary_groups = series.apply(
        lambda x: (
            positive_category_name
            if pd.notna(x) and x >= cutoff_val
            else (negative_category_name if pd.notna(x) else None)
        )
    )
    return binary_groups.rename(f"{series.name}_Group")


def safe_log_p_value(p_value: Optional[float], min_p: float = 1e-10) -> Optional[float]:
    """Calculates -log10(p-value), handling zeros and NaNs."""
    if p_value is None or pd.isna(p_value):
        return None
    p_val_clipped = max(p_value, min_p)
    return -np.log10(p_val_clipped)
