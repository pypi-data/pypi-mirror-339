import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Load environment variables from .env file
if load_dotenv():
    logger.info("Environment variables loaded from .env file")


# Get the environment variables



