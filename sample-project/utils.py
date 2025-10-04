def add(a: int, b: int) -> int:
    """
    Calculates the sum of two integer values.

    :param a: The first integer.
    :param b: The second integer.
    :return: The sum of a and b.
    """
    return a + b

def get_user_greeting(username: str) -> str:
    """
    Generates a personalized greeting message for a user.

    :param username: The name of the user.
    :return: A greeting string, e.g., "Hello, [username]!".
    """
    return f"Hello, {username}!"