#!/usr/bin/env python3
"""
Lucen CLI — The HydraDB Agent Context Layer Command-Line Interface
Inspect, traverse, benchmark, and verify the HydraDB agent context graph directly from terminal.
"""
import sys
import os
import json
import time
import argparse
from typing import Optional

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from backend.hydradb_engine import HydraDBContextEngine
from backend.models import TraversalRequest, FeedbackRequest

# ANSI Color Codes for Clean Terminal Output
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
CYAN = "\033[36m"
WHITE = "\033[37m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"

