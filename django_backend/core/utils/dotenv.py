import os
import re


def is_number(value: str) -> bool:
    """
    Check if the given value can be converted to a number (int or float).

    Args:
        value (str): The value to check.

    Returns:
        bool: True if the value can be converted to a number, otherwise False.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_bool(value: str) -> bool:
    """
    Check if the given value represents a boolean (True or False).

    Args:
        value (str): The value to check.

    Returns:
        bool: True if the value represents a boolean, otherwise False.
    """
    return value.lower() in [str(True).lower(), str(False).lower()]


def str_to_bool(value: str) -> bool:
    """
    Convert a string representation of a boolean to its boolean value.

    Args:
        value (str): The string representation of a boolean.

    Returns:
        bool: The boolean value of the string.
    """
    return value.lower() == str(True).lower()


def str_to_number(value: str):
    """
    Convert a string representation of a number to its int or float value.

    Args:
        value (str): The string representation of a number.

    Returns:
        int/float: The int or float value of the string.
    """
    return int(value) if value.isdigit() else float(value)


def load_env(file_name: str):
    """
    Load environment variables from a file.

    Args:
        file_name (str): The name of the file containing environment variables.

    Raises:
        Exception: If the file does not exist.
    """
    if not os.path.exists(file_name):
        raise Exception(f"Environment config file {file_name} was not found.")

    with open(file_name, "r") as file:
        for line in file:
            result = re.match(
                r"^([a-zA-Z_]+)\s*=\s*([a-zA-Z0-9\-._/()$^&!+*@:%#={}\[\]<>?|~`]*)$",
                line,
            )
            if result:
                os.environ[result.group(1)] = result.group(2)


def get_env_value(var_name: str):
    """
    Retrieve the value of an environment variable, converting it to the appropriate type if necessary.

    Args:
        var_name (str): The name of the environment variable.

    Returns:
        Union[str, int, float, bool, List[str]]: The value of the environment variable.

    Raises:
        Exception: If the environment variable is not set.
    """
    try:
        # Special handling for environment variables that might have comma-separated values.
        if var_name in ["REMOTE_ALLOWED_HOST", "REMOTE_CORS_ORIGIN_WHITELIST"]:
            value = os.environ.get(var_name, "")
        else:
            value = os.environ[var_name]

        # Convert the value to the appropriate type if necessary.
        if is_bool(value):
            return str_to_bool(value)
        elif is_number(value):
            return str_to_number(value)
        return value

    except KeyError:
        raise Exception(f"Set the '{var_name}' environment variable.")
