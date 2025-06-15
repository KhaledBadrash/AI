# utils/validation.py

def validate_id(student_id: str) -> bool:
    """
    Validates that the student ID is numeric and 5–12 digits long.
    """
    return student_id.isdigit() and 5 <= len(student_id) <= 12

def validate_program(program: str, programs: dict) -> bool:
    """
    Checks if the given program exists in HARD_CODED_PROGRAMS.
    """
    return program in programs

def validate_modules(program: str, modules: list, programs: dict) -> bool:
    """
    Ensures each selected module belongs to the chosen program.
    - program: key of HARD_CODED_PROGRAMS
    - modules: list of module names (strings)
    - programs: the HARD_CODED_PROGRAMS dict
    """
    if not modules:
        # no modules selected → still valid
        return True

    allowed = {m['name'] for m in programs[program]['modules']}
    return all(mod in allowed for mod in modules)
