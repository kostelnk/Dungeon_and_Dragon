"""
Utility helpers shared across modules.
"""

def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    """Return Manhattan distance between two (x, y) points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
