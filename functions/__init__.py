import importlib
import inspect
from config import INSTALLED_FUNCTIONS


"""
Aggregate the DEFINITIONS of functions and add functions 
from INSTALLED_FUNCTIONS to the package namespace
"""


DEFINITIONS = []

for module_name in INSTALLED_FUNCTIONS:
    module = importlib.import_module(f"functions.{module_name}")

    # If the module has a DEFINITIONS list, extend the main DEFINITIONS
    if hasattr(module, "DEFINITIONS"):
        DEFINITIONS.extend(module.DEFINITIONS)

    # Get all functions from the module and add them to the package namespace
    for name, func in inspect.getmembers(module, inspect.isfunction):
        globals()[name] = func  # Add function to the current module's globals
