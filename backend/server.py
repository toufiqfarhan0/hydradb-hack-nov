"""
Lucen Backend Server - FastAPI Application for HydraDB Agent Context Layer
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.models import TraversalRequest, TraversalResult, FeedbackRequest
from backend.hydradb_engine import HydraDBContextEngine
