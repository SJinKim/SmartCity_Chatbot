""" 
    in this module are util functions
"""

import os
from typing import Literal
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


def is_result_bescheid(current_response: str) -> bool:
    """
    checks if str parameter is a Bescheid
    Args:
        currentResponse (str): current message

    Returns:
        bool: true if Bescheid
    """
    file_content = current_response.lower()
    if (
        "mit freundlichen gr" in file_content
        and "sehr geehrt" in file_content
        and "rechtsbehelfsbelehrung" in file_content
    ):
        return True
    print("No such words in here Bescheid!")
    return False

def template_concat(prompt_template: str, input_str: str) -> Literal[""]:
    """
    concats input to given prompt template

    Returns:
        Literal: prompt template
    """
    result: str = prompt_template + input_str
    return result
