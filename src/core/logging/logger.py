import structlog

def get_logger(name:str | None= None):
    """
    Return a structured logger.

    Example:
        logger = get_logger(__name__)
    """
    return structlog.get_logger(name)

