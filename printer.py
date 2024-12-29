from pathlib import Path

def log_to_file(message, filex=None):
    """
    Logs a message to both the console and an optional file.

    Args:
        message (str): The message to log.
        filex (file object): An optional file object where the message will be logged.

    Returns:
        None
    """
    print(message)
    if filex:
        print(message, file=filex)


def initialize_output_file(output_path):
    """
    Initializes an output file by creating its parent directories if necessary.

    Args:
        output_path (str or Path): The path to the output file.

    Returns:
        file: A writable file object.
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    return open(output_path, "w")
