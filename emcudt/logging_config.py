import logging


# Configure the logger
def setup_logger(log_file="emcu_debugging_tool.log"):
    """
    Set up the logger for the EMCU Debugging Tool.

    Args:
        log_file (str): The file where logs will be stored.
    """
    logger = logging.getLogger("EmcuDebuggingTool")
    logger.setLevel(logging.DEBUG)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
