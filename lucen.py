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

def print_banner():
    banner = f"""{BOLD}{RED}
    __    __  __  ______  ______    _   __
   / /   / / / / / ____/ / ____/   / | / /
  / /   / / / / / /     / __/     /  |/ / 
 / /___/ /_/ / / /___  / /___    / /|  /  
/_____/\____/  \____/ /_____/   /_/ |_/   {RESET}{DIM}— The HydraDB Agent Context Layer{RESET}
"""
    print(banner)

def cmd_stats(args, engine: HydraDBContextEngine):
    if args.json:
        stats = {
            "servers": len(engine.servers),
            "tools": len(engine.tools),
            "capabilities": len(engine.capabilities),
            "entities": len(engine.entities),
            "edges": len(engine.edges),
            "storage_backend": "SlateDB / MinIO S3",
            "kernel": "SuiteSparse GraphBLAS",
            "accuracy_pct": engine.iteration_history[-1]["accuracy_pct"],
            "token_reduction_pct": engine.iteration_history[-1]["token_reduction_pct"]
        }
        print(json.dumps(stats, indent=2))
        return

    print_banner()
    print(f"{BOLD}HYDRADB GRAPH TOPOLOGY & ENGINE STATUS{RESET}")
    print("=" * 60)
    print(f"  • {BOLD}Engine Kernel:{RESET}      SuiteSparse GraphBLAS (CSC Matrix)")
    print(f"  • {BOLD}Storage Backend:{RESET}    SlateDB LSM-Tree on MinIO / AWS S3")
