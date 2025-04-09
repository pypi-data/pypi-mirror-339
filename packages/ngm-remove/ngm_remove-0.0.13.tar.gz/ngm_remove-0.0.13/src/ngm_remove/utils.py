import os


def exists(path: str) -> bool:
    if os.path.isfile(path):
        return True
    elif os.path.isdir(path):
        return True
    return False


def get_first_part(input_string, delimiter=":"):
    if input_string is None:
        return None

    input_string = input_string.strip()
    parts = input_string.split(delimiter)

    if parts:
        return parts[0]
    else:
        return input_string  # Return the original string if no delimiter found
