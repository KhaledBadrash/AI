# utils/validation.py

import re


def validate_id(student_id: str) -> bool:
    """
    Only digits, exactly 7 characters long.
    """
    return student_id.isdigit() and len(student_id) == 7

def validate_program(program: str, programs_dict: dict) -> bool:
    """
    Program must exist in the hard-coded dictionary.
    """
    return program in programs_dict
