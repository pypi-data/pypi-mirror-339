"""
@fnet/expression Parser Implementation (Python)

IMPORTANT: Function Naming Convention
----------------------------------------------------------------------------
This module uses 'default' (not 'main') as the entry point function because:
1. 'main' in Python is traditionally used with '__main__' for script execution
2. 'default' here indicates a module's primary export/entry point
3. This matches @fnet's auto-detection system for module interfaces
4. Keeps clear separation from Python's if __name__ == '__main__' pattern

The 'default' naming convention allows this module to be used both as:
- A standard Python module with a clear entry point
- A component in the @fnet system's auto-detection framework
"""

import re

def parse_expression(params):
    """
    Recursively parses an expression into processor and statement components.

    Args:
        params (dict): Dictionary containing:
            - expression (str): The expression to parse
            - depth (int, optional): Current recursion depth. Defaults to 5

    Returns:
        dict | None: Parsed components or None if no match or max depth reached.
    """
    expression = params["expression"]
    depth = params.get("depth", 5)

    if depth <= 0:
        return None

    pattern_base = r"^([a-z][a-z0-9_-]*)::([^\s][\s\S]*)$"
    match = re.match(pattern_base, expression)
    if not match:
        return None

    processor, statement = match.groups()
    next_parsed = parse_expression({"expression": statement, "depth": depth - 1})

    result = {
        "processor": processor,
        "statement": statement,
        "expression": expression,
    }

    if next_parsed:
        result["next"] = next_parsed

    return result

def extract_processors(parsed):
    """
    Extracts all processors from a parsed expression.

    Args:
        parsed (dict | None): The parsed expression.

    Returns:
        list[str]: List of processors.
    """
    if not parsed:
        return []

    processors = extract_processors(parsed.get("next", None))
    processors.append(parsed["processor"])  # Fixed: using append() instead of push()
    return processors

def default(params):
    """
    Primary entry point function for expression parsing.
    Named 'default' (not 'main') to:
    1. Avoid confusion with Python's __main__ pattern
    2. Enable @fnet's auto-detection system
    3. Maintain clear module interface

    Args:
        params (dict): Dictionary containing:
            - expression (str): The expression to parse
                Format: processor1::processor2::...::finalStatement

    Returns:
        dict | None: Complete analysis of the expression or None if invalid.
    """
    expression = params["expression"]
    parsed = parse_expression({"expression": expression})

    if not parsed:
        return None

    current = parsed
    while current.get("next"):
        current = current["next"]

    result = {
        "processor": parsed["processor"],
        "statement": parsed["statement"],
        "expression": parsed["expression"],
        "process": {
            "statement": current["statement"],
            "order": extract_processors(parsed),
        }
    }

    if "next" in parsed:
        result["next"] = parsed["next"]

    return result
