# llamacancer/io.py
import logging
import os
import warnings
from typing import Optional

import pandas as pd
from ml_collections import config_dict

from .utils import ensure_numeric


def _load_datafile(
    filepath: str, filetype: Optional[str] = None, **kwargs
) -> Optional[pd.DataFrame]:
    """Generic function to load tabular data with error handling."""
    if not os.path.exists(filepath):
        logging.warning(f"File not found: {filepath}")
        return None

    if filetype is None:
        filetype = os.path.splitext(filepath)[1].lower()

    try:
        logging.info(f"Loading {filepath} as type {filetype}")
        if filetype in [".csv", ".txt", ".tsv"]:
            sep = kwargs.get("sep")
            if sep is None and filetype != ".csv":
                try:
                    df = pd.read_csv(filepath, sep="\t", **kwargs)
                except Exception:
                    df = pd.read_csv(filepath, sep=r"\s+", engine="python", **kwargs)
            else:
                df = pd.read_csv(filepath, **kwargs)
        elif filetype in [".xls", ".xlsx"]:

            df = pd.read_excel(filepath, **kwargs)
        elif filetype in [".parquet", ".pq"]:

            df = pd.read_parquet(filepath, **kwargs)
        else:
            logging.warning(f"Unsupported file type '{filetype}' for {filepath}")
            return None

        logging.info(
            f"Loaded {os.path.basename(filepath)} with {df.shape[0]} rows and {df.shape[1]} columns."
        )
        return df
    except Exception as e:
        logging.error(f"Error loading file {filepath}: {e}", exc_info=True)
        return None


def load_clinical_data(config: config_dict.ConfigDict) -> Optional[pd.DataFrame]:
    """Loads the clinical data file."""
    if not config.get("clinical_file"):
        logging.error("Clinical file not specified in configuration.")
        return None
    filepath = os.path.join(config.data_dir, config.clinical_file)

    req_cols = [config.subject_id_col, config.treatment_arm_col]
    for ep_name, ep_config in config.get("endpoints", {}).items():
        if ep_config.get("time_col"):
            req_cols.append(ep_config.time_col)
        if ep_config.get("status_col"):
            req_cols.append(ep_config.status_col)
        if ep_config.get("response_col"):
            req_cols.append(ep_config.response_col)
    req_cols = list(set(req_cols))

    df = _load_datafile(filepath)
    if df is None:
        return None

    missing = [c for c in req_cols if c not in df.columns]
    if missing:
        logging.error(f"Clinical file missing required columns: {missing}")
        return None

    try:
        df[config.subject_id_col] = df[config.subject_id_col].astype(str)
        df = df.set_index(config.subject_id_col)
    except Exception as e:
        logging.error(f"Error setting index with column '{config.subject_id_col}': {e}")
        return None

    for ep_name, ep_config in config.get("endpoints", {}).items():
        if ep_config.get("time_col") in df.columns:
            df[ep_config.time_col] = ensure_numeric(df[ep_config.time_col], ep_config.time_col)
        if ep_config.get("status_col") in df.columns:
            df[ep_config.status_col] = ensure_numeric(
                df[ep_config.status_col], ep_config.status_col
            )
    return df


def load_biomarker_data(config: config_dict.ConfigDict) -> Optional[pd.DataFrame]:
    """Loads and merges biomarker files."""
    if not config.get("biomarker_files"):
        logging.warning("No biomarker files specified.")
        return None

    all_df = None
    loaded = []
    for name, filename in config.biomarker_files.items():
        if not filename:
            continue
        filepath = os.path.join(config.data_dir, filename)
        df = _load_datafile(filepath)
        if df is None:
            logging.warning(f"Could not load {filename}.")
            continue
        if config.subject_id_col not in df.columns:
            logging.warning(
                f"Biomarker file '{filename}' missing subject ID column '{config.subject_id_col}'."
            )
            continue
        try:
            df[config.subject_id_col] = df[config.subject_id_col].astype(str)
            df = df.set_index(config.subject_id_col)
        except Exception as e:
            logging.error(f"Error setting index in {filename}: {e}")
            continue

        if all_df is None:
            all_df = df
        else:
            overlap = all_df.columns.intersection(df.columns)
            if len(overlap) > 0:
                logging.warning(
                    f"Overlapping columns in '{filename}': {list(overlap)}. Merging with suffix."
                )
                all_df = all_df.join(df, how="outer", lsuffix="_prev", rsuffix=f"_{name}")
            else:
                all_df = all_df.join(df, how="outer")
        loaded.append(filename)
    if all_df is None:
        logging.error("No valid biomarker data loaded.")
    else:
        logging.info(f"Loaded biomarker files: {loaded}")
    return all_df


def merge_clinical_biomarkers(
    clinical_df: pd.DataFrame, biomarker_df: Optional[pd.DataFrame]
) -> pd.DataFrame:
    """Merges clinical and biomarker data via left join."""
    if clinical_df is None:
        raise ValueError("Clinical DataFrame cannot be None.")
    if biomarker_df is None or biomarker_df.empty:
        logging.warning("No biomarker data to merge; returning clinical data only.")
        return clinical_df.copy()
    clinical_df.index = clinical_df.index.astype(str)
    biomarker_df.index = biomarker_df.index.astype(str)
    overlap = clinical_df.columns.intersection(biomarker_df.columns)
    if len(overlap) > 0:
        warnings.warn(f"Overlapping columns: {list(overlap)}. Using suffixes.", UserWarning)
        merged = clinical_df.join(biomarker_df, how="left", lsuffix="_clin", rsuffix="_biom")
    else:
        merged = clinical_df.join(biomarker_df, how="left")
    logging.info(f"Merged data shape: {merged.shape}")
    return merged
