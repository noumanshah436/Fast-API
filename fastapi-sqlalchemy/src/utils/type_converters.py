"""
Type conversion utilities for safe data type conversions.

This module provides utility functions to safely convert values to specific types
while handling None, NaN, and invalid values gracefully.
"""

import math


def safe_str(v):
    """
    Convert value to string, return None if value is None or NaN.

    Args:
        v: Value to convert

    Returns:
        String value with whitespace stripped, or None if value is None/NaN/empty

    Examples:
        >>> safe_str("hello")
        'hello'
        >>> safe_str("  world  ")
        'world'
        >>> safe_str(None)
        None
        >>> safe_str(float('nan'))
        None
        >>> safe_str("")
        None
    """
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    return str(v).strip() if str(v).strip() else None


def safe_int(v):
    """
    Convert value to integer, return None if value is None or NaN.

    Args:
        v: Value to convert

    Returns:
        Integer value, or None if value is None/NaN/invalid

    Examples:
        >>> safe_int(42)
        42
        >>> safe_int("42")
        42
        >>> safe_int(42.9)
        42
        >>> safe_int(None)
        None
        >>> safe_int(float('nan'))
        None
        >>> safe_int("invalid")
        None
    """
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    try:
        return int(v)
    except (ValueError, TypeError):
        return None


def safe_float(v):
    """
    Convert value to float, return None if value is None or NaN.

    Args:
        v: Value to convert

    Returns:
        Float value, or None if value is None/NaN/invalid

    Examples:
        >>> safe_float(42.5)
        42.5
        >>> safe_float("42.5")
        42.5
        >>> safe_float(42)
        42.0
        >>> safe_float(None)
        None
        >>> safe_float(float('nan'))
        None
        >>> safe_float("invalid")
        None
    """
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    try:
        return float(v)
    except (ValueError, TypeError):
        return None


def safe_bool(v):
    """
    Convert value to boolean, return None if value is None or NaN.

    Handles common boolean representations: 'X', 'true', 'True', '1', 1, True, etc.

    Args:
        v: Value to convert

    Returns:
        Boolean value, or None if value is None/NaN/unrecognized

    Examples:
        >>> safe_bool(True)
        True
        >>> safe_bool("X")
        True
        >>> safe_bool("true")
        True
        >>> safe_bool("1")
        True
        >>> safe_bool(1)
        True
        >>> safe_bool(False)
        False
        >>> safe_bool("")
        False
        >>> safe_bool("false")
        False
        >>> safe_bool(0)
        False
        >>> safe_bool(None)
        None
        >>> safe_bool(float('nan'))
        None
    """
    if v is None:
        return None
    if isinstance(v, float) and math.isnan(v):
        return None
    if isinstance(v, bool):
        return v
    if isinstance(v, str):
        v_lower = v.strip().lower()
        if v_lower in ("x", "true", "1", "yes"):
            return True
        if v_lower in ("", "false", "0", "no"):
            return False
        return None
    if isinstance(v, (int, float)):
        return bool(v)
    return None
