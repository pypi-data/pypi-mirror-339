# imports


def compact_time_string(
    time_str: str,
) -> str:
    """
    Convert a string like 'x hour(s) y min(s) z sec(s)' to a HH:MM:SS string.

    Args:
        time_str: A string containing the time in the format 'x hour(s) y min(s) z sec(s)'

    Returns:
        A str representing the time in 'HH:MM:SS' format
    """

    # Split the time string into hours, minutes, and seconds, and remove the word 'hour(s)', 'min(s)', and 'sec(s)'
    parts = time_str.split()
    hours = float(parts[0].replace("hour(s)", ""))
    minutes = float(parts[1].replace("min(s)", ""))
    seconds = float(parts[2].replace("sec(s)", ""))

    return str(f"{hours:02.0f}:{minutes:02.0f}:{seconds:02.0f}")
