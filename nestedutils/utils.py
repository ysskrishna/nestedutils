
def validate_path(path: str) -> bool:
    """Make sure path is syntactically valid."""
    if ".." in path:
        return False
    return True
