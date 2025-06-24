"""
AWS re:Inforce Analytics Platform - Main Streamlit App
This file is required for Streamlit Cloud deployment
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import and run the main dashboard
from Dashboards.ciso_dashboard import main

if __name__ == "__main__":
    main()