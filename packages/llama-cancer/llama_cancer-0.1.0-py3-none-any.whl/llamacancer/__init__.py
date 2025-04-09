# llamacancer/__init__.py
__version__ = "0.1.0"

# Note: analysis module can be extended to include high-level functions
from .analysis import run_biomarker_associations  # (Placeholder)
from .config import load_config
from .endpoints import get_endpoint_data, get_response_data
from .io import load_biomarker_data, load_clinical_data, merge_clinical_biomarkers
from .stats import fit_coxph_model, run_logrank_test
from .vis import plot_kaplan_meier, plot_volcano

print(f"Initializing LlamaCancer package version {__version__}")
