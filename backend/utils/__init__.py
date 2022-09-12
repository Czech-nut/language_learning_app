def snake_to_camel(string: str) -> str:
    """Helper function for converting field names from snake to camel case for FE."""
    parts = "".join(word.capitalize() for word in string.split("_"))
    result = parts[0].lower() + parts[1:]
    return result
