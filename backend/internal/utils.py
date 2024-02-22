""" 
    in this module are util functions
"""
import os
from dotenv import load_dotenv

load_dotenv()

def check_environment():
    """
    checks if the environemt variables are correct

    Raises:
        ValueError: _description_
        ValueError: _description_
    """
    api_key = os.getenv("AZURE_OPENAI_KEY")
    if not api_key:
        raise ValueError("< API Key > nicht gefunden!")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    if not azure_endpoint:
        raise ValueError("< API Endpoint > nicht gefunden!")
    