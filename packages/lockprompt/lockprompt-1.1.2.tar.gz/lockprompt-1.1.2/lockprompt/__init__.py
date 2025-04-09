import os
import logging
import requests

logger = logging.getLogger(__name__)

# Default API base URL (can be overridden)
DEFAULT_API_BASE = os.getenv("LOCKPROMPT_API_BASE", "https://lockprompt.com/api/v1")

def set_api_base(api_base: str):
    """
    Optionally set the base URL for your safety API endpoints.
    """
    global DEFAULT_API_BASE
    DEFAULT_API_BASE = api_base

def is_safe_input(user_input: str, api_base: str = None) -> bool:
    """
    Checks if a user input is safe by calling the /check-safe-input endpoint.
    Returns True if safe, False if unsafe or on error.
    """
    if api_base is None:
        api_base = DEFAULT_API_BASE
    url = f"{api_base.rstrip('/')}/check-safe-input"
    payload = {"user_input": user_input}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("is_safe", False)
    except Exception as e:
        logger.error(f"[lockprompt] is_safe_input() error: {e}")
        return False

def is_safe_output(llm_output: str, api_base: str = None) -> bool:
    """
    Checks if an LLM output is safe by calling the /check-safe-output endpoint.
    Returns True if safe, False if unsafe or on error.
    """
    if api_base is None:
        api_base = DEFAULT_API_BASE
    url = f"{api_base.rstrip('/')}/check-safe-output"
    payload = {"llm_output": llm_output}
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        data = response.json()
        return data.get("is_safe", False)
    except Exception as e:
        logger.error(f"[lockprompt] is_safe_output() error: {e}")
        return False
