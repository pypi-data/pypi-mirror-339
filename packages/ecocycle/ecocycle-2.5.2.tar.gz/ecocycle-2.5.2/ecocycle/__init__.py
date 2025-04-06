"""
EcoCycle - Cycle into a greener tomorrow

A program for tracking cycling activities, calculating environmental benefits,
and managing user data through Google Sheets integration.
"""

__version__ = "2.5"
__author__ = "Shirish Pothi"

# Use relative import since this file is inside the ecocycle package
from .main import main_program

# Define what symbols are exported when using "from ecocycle import *"
__all__ = ['main_program']