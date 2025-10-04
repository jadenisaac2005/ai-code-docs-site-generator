# main.py content:
# Note: The import is relative, assuming a standard Python package structure.
# For a simple hackathon test, this might need adjustment based on the generator script's run location.
# We will assume the generator handles the path correctly.

def calculate_area(length: float, width: float) -> float:
    """
    Computes the area of a rectangle.

    :param length: The length of the rectangle.
    :param width: The width of the rectangle.
    :return: The calculated area.
    """
    return length * width

def is_positive(number: int) -> bool:
    """
    Checks if a given number is strictly positive.

    :param number: The integer to check.
    :return: True if the number is greater than 0, False otherwise.
    """
    return number > 0