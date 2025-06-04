import logging
import os
from pathlib import Path

from dotenv import load_dotenv

is_dotenv_loaded = load_dotenv()

MODEL_CACHE_DIR = Path("./models")

GRPC_PORT = os.getenv("GRPC_PORT")
LOG_LEVEL = os.getenv("LOG_LEVEL", logging.WARNING)
if LOG_LEVEL not in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
    error_msg = "LOG_LEVEL must be one of: DEBUG, INFO, WARNING, ERROR, CRITICAL"
    raise ValueError(error_msg)

SEQ_URL = os.getenv("SEQ_URL")
