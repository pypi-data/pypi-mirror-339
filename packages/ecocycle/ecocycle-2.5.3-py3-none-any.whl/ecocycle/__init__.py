"""
EcoCycle - Cycle into a greener tomorrow

A program for tracking cycling activities, calculating environmental benefits,
and managing user data through Google Sheets integration.
"""

__version__ = "2.5.3"
__author__ = "Shirish Pothi"

# Import and expose the main_program function at the module level
from .main import main_program

# Define what symbols are exported when using "from ecocycle import *"
__all__ = ['main_program']