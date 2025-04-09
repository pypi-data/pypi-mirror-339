# llamacancer/endpoints.py
import logging
import warnings
from typing import Optional, Tuple

import numpy as np
import pandas as pd


def check_endpoint_columns(df: pd.DataFrame, ep_config: dict, ep_name: str) -> bool:
    """Checks if required columns for an endpoint exist."""
    time_col = ep_config.get("time_col")
    status_col = ep_config.get("status_col")
    response_col = ep_config.get("response_col")
    valid = True
    if time_col and time_col not in df.columns:
        logging.error(f"Endpoint '{ep_name}': Missing time column '{time_col}'.")
        valid = False
    if status_col and status_col not in df.columns:
        logging.error(f"Endpoint '{ep_name}': Missing status column '{status_col}'.")
        valid = False
    if response_col and response_col not in df.columns:
        logging.error(f"Endpoint '{ep_name}': Missing response column '{response_col}'.")
        valid = False

    if time_col in df.columns and not pd.api.types.is_numeric_dtype(df[time_col]):
        logging.warning(f"Endpoint '{ep_name}': Time column '{time_col}' is not numeric.")
    if status_col in df.columns and not pd.api.types.is_numeric_dtype(df[status_col]):
        try:
            df[status_col] = (
                df[status_col].map({True: 1, False: 0, "1": 1, "0": 0}).fillna(-1).astype(int)
            )
            if (df[status_col] == -1).any():
                raise ValueError("Mapping failed")
            if not df[status_col].isin([0, 1]).all():
                raise ValueError("Status must be 0 or 1")
            logging.info(f"Converted status column '{status_col}' to numeric.")
        except Exception:
            logging.warning(f"Endpoint '{ep_name}': Status column '{status_col}' is not numeric.")
    return valid


def get_endpoint_data(
    df: pd.DataFrame, endpoint_name: str, config: object
) -> Optional[Tuple[pd.Series, pd.Series]]:
    """Extracts time and status columns for a survival endpoint."""
    ep_config = config.endpoints.get(endpoint_name)
    if not ep_config:
        logging.error(f"Endpoint '{endpoint_name}' not defined in configuration.")
        return None
    if not check_endpoint_columns(df, ep_config, endpoint_name):
        return None
    return df[ep_config.time_col], df[ep_config.status_col]


def get_response_data(
    df: pd.DataFrame, endpoint_name: str = "response", config: object = None
) -> Optional[pd.Series]:
    """Extracts and optionally binarizes a response endpoint."""
    ep_config = config.endpoints.get(endpoint_name)
    if not ep_config:
        logging.error(f"Response endpoint '{endpoint_name}' not defined in configuration.")
        return None
    if not check_endpoint_columns(df, ep_config, endpoint_name):
        return None
    response_col = ep_config.response_col
    resp_series = df[response_col]
    positive_values = ep_config.get("positive_values")
    if positive_values and isinstance(positive_values, list):
        resp_series_str = resp_series.astype(str).str.strip().str.lower()
        pos_vals_lower = [str(v).strip().lower() for v in positive_values]
        binary_response = resp_series_str.isin(pos_vals_lower).astype(int)
        binary_response[resp_series.isna()] = np.nan
        logging.info(f"Binarized response column '{response_col}' using values: {positive_values}")
        return binary_response
    else:
        if not resp_series.dropna().isin([0, 1]).all():
            warnings.warn(
                f"Response column '{response_col}' is not binary and no positive_values provided.",
                UserWarning,
            )
        return resp_series
