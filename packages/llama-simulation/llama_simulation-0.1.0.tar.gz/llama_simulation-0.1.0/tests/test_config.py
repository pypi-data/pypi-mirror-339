"""Configuration for pytest."""

import os
import sys
from pathlib import Path

# Add the root directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set environment variables for testing
os.environ["LLAMA_SIM_LOG_LEVEL"] = "DEBUG"
os.environ["LLAMA_SIM_DEVICE"] = "cpu"
os.environ["LLAMA_SIM_RESULT_DIR"] = "./test_results"
os.environ["LLAMA_SIM_SEED"] = "42"
