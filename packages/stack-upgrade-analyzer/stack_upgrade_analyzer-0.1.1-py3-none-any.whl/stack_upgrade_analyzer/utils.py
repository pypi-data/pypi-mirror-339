"""
Utility functions for the Stack Upgrade Analyzer.
"""

import os
from pathlib import Path

def get_package_root():
    """Return the root directory of the package."""
    return Path(__file__).resolve().parent

def get_data_dir():
    """Return the data directory of the package."""
    return get_package_root() / "data"

def get_changes_dir(stack="node"):
    """Return the changes directory for a specific stack."""
    return get_data_dir() / "changes" / stack
