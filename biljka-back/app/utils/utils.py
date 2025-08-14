# app/utils/utils.py

from fastapi import Request
import logging

def log_request_data(request: Request):
    """
    Loguje osnovne informacije o zahtevu.
    """
    logging.info(f"{request.method} request to {request.url}")

def format_status(input_value: str) -> str:
    """
    Normalizuje status (npr. 'dobar', 'Dobar' → 'Dobar')
    """
    return input_value.strip().capitalize()

def is_valid_age(age: int) -> bool:
    """
    Prosta validacija godine.
    """
    return 0 < age < 120
