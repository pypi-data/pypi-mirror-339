"""
Git Repository Intelligence Platform - A Python package for AI-driven Git repository analysis
"""

from .version import __version__

# Instead of importing from git_repo_intelligence (which causes circular import),
# we'll make these available through the package by importing them directly in __init__
import sys
import os
import importlib.util

# Dynamically import the module to avoid circular imports
spec = importlib.util.spec_from_file_location("git_repo_intelligence_main", 
                                             os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                                                         "git_repo_intelligence.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Now expose the functions at the package level
run_analysis = module.run_analysis
main = module.main 