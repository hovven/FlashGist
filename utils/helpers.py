import os
import logging


def setup_logging():
    log_directory = 'logs'
    log_filename = 'app.log'
    full_log_path = os.path.join(log_directory, log_filename)

    # Check if the logs directory exists, and create it if it doesn't
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    logger = logging.getLogger(__name__)

    # Use full_log_path instead of 'logs/app.log'
    logging.basicConfig(
        filename=full_log_path,
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] - %(message)s'
    )

    file_handler = logging.FileHandler(full_log_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(file_handler)

    return logging
